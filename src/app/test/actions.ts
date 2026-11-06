"use server";

import { revalidatePath } from "next/cache";
import { createClient } from "@/utils/supabase/server";
import type { Question, QuestionOption, RawQuestionOption } from "@/types/database";

export type QuestionFilterMode = "all" | "incorrect" | "unseen";

export interface ActiveTestQuestion {
  id: string;
  category_id: string;
  categoryName?: string;
  subjectName?: string;
  content: string;
  options: QuestionOption[];
  isMultipleChoice: boolean;
}

export interface TestSubmissionItem {
  questionId: string;
  selectedOptionIds: string[];
}

export interface EvaluatedQuestionResult {
  questionId: string;
  content: string;
  options: QuestionOption[];
  selectedOptionIds: string[];
  correctAnswers: string[];
  isCorrect: boolean;
  explanation: string | null;
}

export interface TestEvaluationSummary {
  totalQuestions: number;
  correctCount: number;
  scorePercentage: number;
  results: EvaluatedQuestionResult[];
}

function normalizeOptions(rawOptions: RawQuestionOption[]): QuestionOption[] {
  if (!Array.isArray(rawOptions)) return [];
  return rawOptions.map((opt, idx) => {
    if (typeof opt === "string") {
      return { id: opt, text: opt };
    }
    return {
      id: String(opt.id ?? idx),
      text: String(opt.text ?? ""),
    };
  });
}

function shuffleArray<T>(items: T[]): T[] {
  const copy = [...items];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

/**
 * 1. Načíta a vyfiltruje otázky pre Test Builder podľa:
 *    - zvolených kategórií (categoryIds)
 *    - filtra ("all" | "incorrect" | "unseen") s využitím tabuľky `user_progress`
 *    - počtu otázok (limit: napr. 10, 20, 50)
 * Nevracia správne odpovede ani vysvetlenia počas samotného testu.
 */
export async function generateTestQuestionsAction(params: {
  categoryIds: string[];
  questionCount: number;
  filterMode: QuestionFilterMode;
}): Promise<{
  questions?: ActiveTestQuestion[];
  error?: string;
}> {
  try {
    const supabase = createClient();
    const {
      data: { user },
      error: authError,
    } = await supabase.auth.getUser();

    if (authError || !user) {
      return { error: "Pre spustenie testu sa musíte prihlásiť." };
    }

    const { categoryIds, questionCount, filterMode } = params;

    if (!Array.isArray(categoryIds) || categoryIds.length === 0) {
      return { error: "Vyberte aspoň jednu kategóriu otázok." };
    }

    const validLimit = Math.max(1, Math.min(200, Number(questionCount) || 10));

    // Načítanie kandidátskych otázok z vybraných kategórií
    const { data: rawQuestions, error: questionsError } = await supabase
      .from("questions")
      .select("id, category_id, content, options, correct_answers")
      .in("category_id", categoryIds);

    if (questionsError) {
      return {
        error: `Chyba pri načítaní otázok: ${questionsError.message}`,
      };
    }

    if (!rawQuestions || rawQuestions.length === 0) {
      return {
        error: "Vo vybraných kategóriách sa zatiaľ nenachádzajú žiadne otázky.",
      };
    }

    let filteredQuestions = rawQuestions as Pick<
      Question,
      "id" | "category_id" | "content" | "options" | "correct_answers"
    >[];

    // Ak je zvolený filter "incorrect" alebo "unseen", dopytujeme `user_progress`
    if (filterMode === "incorrect" || filterMode === "unseen") {
      const candidateIds = filteredQuestions.map((q) => q.id);

      const { data: progressRows, error: progressError } = await supabase
        .from("user_progress")
        .select("question_id, is_correct, created_at")
        .eq("user_id", user.id)
        .in("question_id", candidateIds)
        .order("created_at", { ascending: false });

      if (progressError) {
        return {
          error: `Chyba pri filtrovaní progresu používateľa: ${progressError.message}`,
        };
      }

      if (filterMode === "unseen") {
        // Nové (ešte nevidené): otázky, ktoré nemajú žiadny záznam v user_progress
        const seenQuestionIds = new Set(
          (progressRows ?? []).map((row) => row.question_id)
        );
        filteredQuestions = filteredQuestions.filter(
          (q) => !seenQuestionIds.has(q.id)
        );
      } else if (filterMode === "incorrect") {
        // Iba nesprávne zodpovedané: sledujeme poslednú odpoveď používateľa na danú otázku
        const latestStatusByQuestion = new Map<string, boolean>();
        for (const row of progressRows ?? []) {
          if (!latestStatusByQuestion.has(row.question_id)) {
            latestStatusByQuestion.set(row.question_id, Boolean(row.is_correct));
          }
        }

        filteredQuestions = filteredQuestions.filter(
          (q) => latestStatusByQuestion.get(q.id) === false
        );
      }
    }

    if (filteredQuestions.length === 0) {
      const filterLabel =
        filterMode === "unseen"
          ? "Nové (ešte nevidené)"
          : filterMode === "incorrect"
            ? "Iba nesprávne zodpovedané"
            : "Všetky";
      return {
        error: `Pre zvolený filter „${filterLabel}“ sa vo vybraných kategóriách nenašli žiadne otázky.`,
      };
    }

    // Náhodne premiešame otázky a orežeme na požadovaný počet
    const selectedQuestions = shuffleArray(filteredQuestions).slice(
      0,
      validLimit
    );

    const activeQuestions: ActiveTestQuestion[] = selectedQuestions.map((q) => {
      const correctArr = Array.isArray(q.correct_answers)
        ? q.correct_answers
        : [];
      return {
        id: q.id,
        category_id: q.category_id,
        content: q.content,
        options: normalizeOptions(q.options),
        isMultipleChoice: correctArr.length > 1,
      };
    });

    return { questions: activeQuestions };
  } catch (err) {
    return {
      error:
        err instanceof Error
          ? err.message
          : "Nastala neočakávaná chyba pri vytváraní testu.",
    };
  }
}

/**
 * 2. Vyhodnotí odoslaný test a zapíše každý záznam (správne/nesprávne)
 *    do tabuľky `user_progress` v Supabase.
 */
export async function evaluateTestAction(
  submissions: TestSubmissionItem[]
): Promise<{
  evaluation?: TestEvaluationSummary;
  error?: string;
}> {
  try {
    const supabase = createClient();
    const {
      data: { user },
      error: authError,
    } = await supabase.auth.getUser();

    if (authError || !user) {
      return { error: "Pre vyhodnotenie testu sa musíte prihlásiť." };
    }

    if (!Array.isArray(submissions) || submissions.length === 0) {
      return { error: "Test neobsahuje žiadne otázky na vyhodnotenie." };
    }

    const questionIds = submissions.map((s) => s.questionId);

    const { data: dbQuestions, error: dbError } = await supabase
      .from("questions")
      .select("id, content, options, correct_answers, explanation")
      .in("id", questionIds);

    if (dbError || !dbQuestions) {
      return {
        error: `Nepodarilo sa načítať správne odpovede z databázy: ${
          dbError?.message ?? "Neznáma chyba"
        }`,
      };
    }

    const questionMap = new Map(
      (dbQuestions as Question[]).map((q) => [q.id, q] as const)
    );

    const results: EvaluatedQuestionResult[] = [];
    const progressRowsToInsert: {
      user_id: string;
      question_id: string;
      is_correct: boolean;
    }[] = [];

    let correctCount = 0;

    for (const sub of submissions) {
      const q = questionMap.get(sub.questionId);
      if (!q) continue;

      const correctAnswers = (
        Array.isArray(q.correct_answers) ? q.correct_answers : []
      ).map((ans) => String(ans));

      const correctSet = new Set(correctAnswers);
      const selectedUnique = Array.from(
        new Set((sub.selectedOptionIds ?? []).map((id) => String(id)))
      );

      const isCorrect =
        selectedUnique.length === correctSet.size &&
        selectedUnique.every((id) => correctSet.has(id));

      if (isCorrect) {
        correctCount++;
      }

      results.push({
        questionId: q.id,
        content: q.content,
        options: normalizeOptions(q.options),
        selectedOptionIds: selectedUnique,
        correctAnswers,
        isCorrect,
        explanation: q.explanation ?? null,
      });

      progressRowsToInsert.push({
        user_id: user.id,
        question_id: q.id,
        is_correct: isCorrect,
      });
    }

    if (progressRowsToInsert.length > 0) {
      const { error: insertProgressError } = await supabase
        .from("user_progress")
        .insert(progressRowsToInsert);

      if (insertProgressError) {
        return {
          error: `Chyba pri ukladaní výsledkov do user_progress: ${insertProgressError.message}`,
        };
      }
    }

    revalidatePath("/");
    revalidatePath("/test");

    const totalQuestions = results.length;
    const scorePercentage =
      totalQuestions > 0
        ? Math.round((correctCount / totalQuestions) * 100)
        : 0;

    return {
      evaluation: {
        totalQuestions,
        correctCount,
        scorePercentage,
        results,
      },
    };
  } catch (err) {
    return {
      error:
        err instanceof Error
          ? err.message
          : "Nastala neočakávaná chyba pri vyhodnocovaní testu.",
    };
  }
}

