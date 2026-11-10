"use server";

import { revalidatePath } from "next/cache";
import { createClient } from "@/utils/supabase/server";
import { isAdminEmail } from "@/lib/admin";
import type { BulkImportQuestionItem } from "@/types/database";

async function requireAdminSupabase() {
  const supabase = createClient();
  const {
    data: { user },
    error: authError,
  } = await supabase.auth.getUser();

  if (authError || !user) {
    throw new Error("Nie ste prihlásený.");
  }

  if (!isAdminEmail(user.email)) {
    throw new Error(
      `Prístup zamietnutý. Prihlásený účet (${user.email}) nemá administrátorské oprávnenie.`
    );
  }

  return { supabase, user };
}

export async function createSubjectAndCategoryAction(
  subjectName: string,
  categoryName: string
) {
  try {
    const { supabase } = await requireAdminSupabase();

    const cleanSubject = subjectName.trim();
    const cleanCategory = categoryName.trim();

    if (!cleanSubject || !cleanCategory) {
      return { error: "Zadajte názov predmetu aj názov kategórie." };
    }

    // 1. Nájsť alebo vytvoriť predmet
    let { data: subjectData, error: subjectSelectError } = await supabase
      .from("subjects")
      .select("id, name")
      .ilike("name", cleanSubject)
      .maybeSingle();

    if (subjectSelectError) {
      return { error: `Chyba pri hľadaní predmetu: ${subjectSelectError.message}` };
    }

    if (!subjectData) {
      const { data: createdSubject, error: createSubjectError } = await supabase
        .from("subjects")
        .insert({ name: cleanSubject })
        .select("id, name")
        .single();

      if (createSubjectError || !createdSubject) {
        return {
          error: `Nepodarilo sa vytvoriť predmet: ${
            createSubjectError?.message ?? "Neznáma chyba"
          }`,
        };
      }
      subjectData = createdSubject;
    }

    // 2. Nájsť alebo vytvoriť kategóriu pod predmetom
    let { data: categoryData, error: categorySelectError } = await supabase
      .from("categories")
      .select("id, subject_id, name")
      .eq("subject_id", subjectData.id)
      .ilike("name", cleanCategory)
      .maybeSingle();

    if (categorySelectError) {
      return {
        error: `Chyba pri hľadaní kategórie: ${categorySelectError.message}`,
      };
    }

    if (!categoryData) {
      const { data: createdCategory, error: createCategoryError } =
        await supabase
          .from("categories")
          .insert({
            subject_id: subjectData.id,
            name: cleanCategory,
          })
          .select("id, subject_id, name")
          .single();

      if (createCategoryError || !createdCategory) {
        return {
          error: `Nepodarilo sa vytvoriť kategóriu: ${
            createCategoryError?.message ?? "Neznáma chyba"
          }`,
        };
      }
      categoryData = createdCategory;
    }

    revalidatePath("/admin");
    revalidatePath("/");

    return {
      success: `Predmet "${subjectData.name}" a kategória "${categoryData.name}" sú pripravené.`,
      categoryId: categoryData.id,
    };
  } catch (err) {
    return {
      error: err instanceof Error ? err.message : "Nastala neočakávaná chyba.",
    };
  }
}

export async function importQuestionsFromJsonAction(
  rawJson: string,
  fallbackCategoryId?: string
) {
  try {
    const { supabase } = await requireAdminSupabase();

    if (!rawJson || !rawJson.trim()) {
      return { error: "JSON pole nemôže byť prázdne." };
    }

    let parsed: unknown;
    try {
      parsed = JSON.parse(rawJson);
    } catch (parseErr) {
      return {
        error: `Neplatný formát JSON: ${
          parseErr instanceof Error ? parseErr.message : "Syntaktická chyba"
        }`,
      };
    }

    // Podpora pre čisté pole [...] aj objekt { "questions": [...] }
    const items: unknown[] = Array.isArray(parsed)
      ? parsed
      : parsed &&
          typeof parsed === "object" &&
          "questions" in parsed &&
          Array.isArray((parsed as { questions: unknown[] }).questions)
        ? (parsed as { questions: unknown[] }).questions
        : [];

    if (items.length === 0) {
      return {
        error:
          "JSON musí obsahovať neprázdne pole otázok (napr. [ { ... } ] alebo { \"questions\": [ ... ] }).",
      };
    }

    // Cache pre automatické vytváranie/hľadanie predmetov a kategórií podľa názvu
    const subjectCache = new Map<string, string>();
    const categoryCache = new Map<string, string>();

    const { data: existingSubjects } = await supabase
      .from("subjects")
      .select("id, name");
    existingSubjects?.forEach((s) =>
      subjectCache.set(s.name.trim().toLowerCase(), s.id)
    );

    const { data: existingCategories } = await supabase
      .from("categories")
      .select("id, subject_id, name");
    existingCategories?.forEach((c) =>
      categoryCache.set(`${c.subject_id}::${c.name.trim().toLowerCase()}`, c.id)
    );

    const rowsToInsert: {
      category_id: string;
      content: string;
      options: unknown[];
      correct_answers: unknown[];
      explanation: string | null;
    }[] = [];

    for (let i = 0; i < items.length; i++) {
      const rawItem = items[i] as Partial<BulkImportQuestionItem>;
      const indexLabel = `Otázka #${i + 1}`;

      if (!rawItem || typeof rawItem !== "object") {
        return { error: `${indexLabel} nie je platný JSON objekt.` };
      }

      const content =
        typeof rawItem.content === "string" ? rawItem.content.trim() : "";
      if (!content) {
        return { error: `${indexLabel}: chýba text otázky ("content").` };
      }

      if (!Array.isArray(rawItem.options) || rawItem.options.length < 2) {
        return {
          error: `${indexLabel}: pole "options" musí obsahovať aspoň 2 možnosti.`,
        };
      }

      if (
        !Array.isArray(rawItem.correct_answers) ||
        rawItem.correct_answers.length === 0
      ) {
        return {
          error: `${indexLabel}: pole "correct_answers" musí byť neprázdne pole správnych odpovedí.`,
        };
      }

      let categoryId =
        typeof rawItem.category_id === "string" && rawItem.category_id.trim()
          ? rawItem.category_id.trim()
          : fallbackCategoryId?.trim() || "";

      // Ak otázka obsahuje názov `subject` a `category`, automaticky ich nájdeme alebo vytvoríme
      if (!categoryId && rawItem.subject && rawItem.category) {
        const subjName = String(rawItem.subject).trim();
        const catName = String(rawItem.category).trim();
        const subjKey = subjName.toLowerCase();

        let subjectId: string | undefined = subjectCache.get(subjKey);
        if (!subjectId) {
          const { data: newSubj, error: subjErr } = await supabase
            .from("subjects")
            .insert({ name: subjName })
            .select("id")
            .single();

          if (subjErr || !newSubj || !newSubj.id) {
            return {
              error: `${indexLabel}: nepodarilo sa vytvoriť predmet "${subjName}" (${
                subjErr?.message ?? "skontrolujte RLS politiku pre admina"
              }).`,
            };
          }
          subjectId = String(newSubj.id);
          subjectCache.set(subjKey, subjectId);
        }

        const catKey = `${subjectId}::${catName.toLowerCase()}`;
        let resolvedCatId: string | undefined = categoryCache.get(catKey);
        if (!resolvedCatId) {
          const { data: newCat, error: catErr } = await supabase
            .from("categories")
            .insert({ subject_id: subjectId, name: catName })
            .select("id")
            .single();

          if (catErr || !newCat || !newCat.id) {
            return {
              error: `${indexLabel}: nepodarilo sa vytvoriť kategóriu "${catName}" (${
                catErr?.message ?? "skontrolujte RLS politiku pre admina"
              }).`,
            };
          }
          resolvedCatId = String(newCat.id);
          categoryCache.set(catKey, resolvedCatId);
        }

        categoryId = resolvedCatId;
      }

      if (!categoryId) {
        return {
          error: `${indexLabel}: chýba "category_id" (vyberte cieľovú kategóriu hore alebo uveďte "subject" a "category" priamo v JSONe).`,
        };
      }

      rowsToInsert.push({
        category_id: categoryId,
        content,
        options: rawItem.options,
        correct_answers: rawItem.correct_answers.map((ans) => String(ans)),
        explanation:
          typeof rawItem.explanation === "string" && rawItem.explanation.trim()
            ? rawItem.explanation.trim()
            : null,
      });
    }

    const { data: inserted, error: insertError } = await supabase
      .from("questions")
      .insert(rowsToInsert)
      .select("id");

    if (insertError) {
      return {
        error: `Chyba pri ukladaní do Supabase: ${insertError.message}`,
      };
    }

    revalidatePath("/admin");
    revalidatePath("/");

    return {
      success: `Úspešne naimportovaných ${
        inserted?.length ?? rowsToInsert.length
      } otázok do databázy Supabase!`,
      count: inserted?.length ?? rowsToInsert.length,
    };
  } catch (err) {
    return {
      error: err instanceof Error ? err.message : "Nastala neočakávaná chyba.",
    };
  }
}

export async function updateUserApprovalStatusAction(
  userId: string,
  newStatus: "approved" | "rejected" | "pending"
) {
  try {
    const { supabase } = await requireAdminSupabase();

    const { error } = await supabase
      .from("profiles")
      .update({
        status: newStatus,
        updated_at: new Date().toISOString(),
      })
      .eq("id", userId);

    if (error) {
      return { error: `Chyba pri aktualizácii stavu: ${error.message}` };
    }

    revalidatePath("/admin");
    revalidatePath("/pending-approval");

    const statusLabels: Record<string, string> = {
      approved: "schválený",
      rejected: "zamietnutý",
      pending: "vrátený medzi čakajúce",
    };

    return {
      success: `Používateľ bol úspešne ${statusLabels[newStatus] ?? newStatus}.`,
    };
  } catch (err) {
    return {
      error: err instanceof Error ? err.message : "Nastala neočakávaná chyba.",
    };
  }
}

export async function deleteUserProfileAction(userId: string) {
  try {
    const { supabase } = await requireAdminSupabase();

    const { error } = await supabase.from("profiles").delete().eq("id", userId);

    if (error) {
      return { error: `Chyba pri odstraňovaní profilu: ${error.message}` };
    }

    revalidatePath("/admin");
    return { success: "Používateľský záznam bol odstránený." };
  } catch (err) {
    return {
      error: err instanceof Error ? err.message : "Nastala neočakávaná chyba.",
    };
  }
}

// ============================================================================
// NAHLÁSENÉ OTÁZKY (FLAGGED QUESTIONS)
// ============================================================================

export async function flagQuestionAction(params: {
  questionId: string;
  reason?: string;
}) {
  try {
    const supabase = createClient();
    const {
      data: { user },
    } = await supabase.auth.getUser();

    const { error } = await supabase.from("flagged_questions").insert({
      question_id: params.questionId,
      user_id: user?.id ?? null,
      user_email: user?.email ?? "Anonymný používateľ",
      reason: params.reason?.trim() || "Nahlásená chyba v otázke",
      status: "pending",
    });

    if (error) {
      // Ak tabuľka zatiaľ neexistuje, vrátime zrozumiteľnú správu
      if (error.code === "42P01" || error.message.includes("does not exist")) {
        return {
          error:
            "Systém nahlasovania zatiaľ nebol aktivovaný v databáze (chýba tabuľka flagged_questions). Administrátor musí spustiť skript zo schema.sql.",
        };
      }
      return { error: `Chyba pri odosielaní nahlásenia: ${error.message}` };
    }

    revalidatePath("/admin");
    return {
      success:
        "Otázka bola úspešne nahlásená a administrátor ju preverí v administrátorskom paneli.",
    };
  } catch (err) {
    return {
      error: err instanceof Error ? err.message : "Nastala neočakávaná chyba.",
    };
  }
}

export async function updateFlaggedQuestionStatusAction(
  flagId: string,
  newStatus: "pending" | "resolved" | "dismissed"
) {
  try {
    const { supabase } = await requireAdminSupabase();
    const { error } = await supabase
      .from("flagged_questions")
      .update({
        status: newStatus,
        resolved_at: newStatus !== "pending" ? new Date().toISOString() : null,
      })
      .eq("id", flagId);

    if (error) {
      return { error: `Chyba pri aktualizácii stavu nahlásenia: ${error.message}` };
    }

    revalidatePath("/admin");
    const label =
      newStatus === "resolved"
        ? "označené ako vyriešené"
        : newStatus === "dismissed"
        ? "zamietnuté"
        : "vrátené medzi čakajúce";
    return { success: `Nahlásenie bolo ${label}.` };
  } catch (err) {
    return {
      error: err instanceof Error ? err.message : "Nastala neočakávaná chyba.",
    };
  }
}

export async function updateQuestionDetailsAction(params: {
  questionId: string;
  content: string;
  options: { id: string; text: string }[];
  correctAnswers: string[];
  explanation?: string;
  resolveFlagId?: string;
}) {
  try {
    const { supabase } = await requireAdminSupabase();

    const { error: updateError } = await supabase
      .from("questions")
      .update({
        content: params.content.trim(),
        options: params.options,
        correct_answers: params.correctAnswers,
        explanation: params.explanation?.trim() || null,
      })
      .eq("id", params.questionId);

    if (updateError) {
      return { error: `Chyba pri ukladaní otázky: ${updateError.message}` };
    }

    if (params.resolveFlagId) {
      await supabase
        .from("flagged_questions")
        .update({
          status: "resolved",
          resolved_at: new Date().toISOString(),
        })
        .eq("id", params.resolveFlagId);
    }

    revalidatePath("/admin");
    revalidatePath("/test");
    return {
      success:
        "Otázka bola úspešne upravená v databáze a nahlásenie bolo vyriešené.",
    };
  } catch (err) {
    return {
      error: err instanceof Error ? err.message : "Nastala neočakávaná chyba.",
    };
  }
}

export async function deleteFlaggedQuestionAction(flagId: string) {
  try {
    const { supabase } = await requireAdminSupabase();
    const { error } = await supabase
      .from("flagged_questions")
      .delete()
      .eq("id", flagId);

    if (error) {
      return { error: `Chyba pri zmazaní nahlásenia: ${error.message}` };
    }

    revalidatePath("/admin");
    return { success: "Nahlásenie bolo úspešne odstránené." };
  } catch (err) {
    return {
      error: err instanceof Error ? err.message : "Nastala neočakávaná chyba.",
    };
  }
}



