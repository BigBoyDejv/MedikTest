import { redirect } from "next/navigation";
import { createClient } from "@/utils/supabase/server";
import {
  TestSuite,
  type SubjectGroup,
} from "@/components/test/test-suite";
import type { QuestionFilterMode } from "@/app/test/actions";
import { Badge } from "@/components/ui/badge";
import { ClipboardList } from "lucide-react";

export const dynamic = "force-dynamic";

interface TestPageProps {
  searchParams?: {
    category?: string;
    categories?: string;
    subject?: string;
    filter?: string;
  };
}

export default async function TestPage({ searchParams }: TestPageProps) {
  const supabase = createClient();

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    redirect("/login?next=/test");
  }

  const [{ data: subjects }, { data: categories }, { data: questionRows }] =
    await Promise.all([
      supabase.from("subjects").select("id, name").order("name"),
      supabase
        .from("categories")
        .select("id, subject_id, name")
        .order("name"),
      supabase.from("questions").select("id, category_id"),
    ]);

  // Spočítame počet otázok v každej kategórii
  const countByCategoryId = new Map<string, number>();
  for (const row of questionRows ?? []) {
    countByCategoryId.set(
      row.category_id,
      (countByCategoryId.get(row.category_id) ?? 0) + 1
    );
  }

  const subjectGroups: SubjectGroup[] = (subjects ?? []).map((subj) => {
    const subjCategories = (categories ?? [])
      .filter((cat) => cat.subject_id === subj.id)
      .map((cat) => ({
        id: cat.id,
        subject_id: cat.subject_id,
        name: cat.name,
        questionCount: countByCategoryId.get(cat.id) ?? 0,
      }));

    return {
      id: subj.id,
      name: subj.name,
      categories: subjCategories,
    };
  });

  // Predvýber kategórií z URL parametrov (?categories=id1,id2 alebo ?category=id1 alebo ?subject=id)
  let initialSelectedCategoryIds: string[] | undefined;
  if (searchParams?.categories) {
    const parsedIds = searchParams.categories
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);
    if (parsedIds.length > 0) {
      initialSelectedCategoryIds = parsedIds;
    }
  } else if (searchParams?.category) {
    initialSelectedCategoryIds = [searchParams.category];
  } else if (searchParams?.subject) {
    const matching = (categories ?? [])
      .filter((c) => c.subject_id === searchParams.subject)
      .map((c) => c.id);
    if (matching.length > 0) {
      initialSelectedCategoryIds = matching;
    }
  }

  // Predvýber filtra z URL parametra (?filter=incorrect | unseen | all)
  const rawFilter = searchParams?.filter;
  const initialFilterMode: QuestionFilterMode | undefined =
    rawFilter === "incorrect" || rawFilter === "unseen" || rawFilter === "all"
      ? rawFilter
      : undefined;

  return (
    <main className="mx-auto max-w-5xl space-y-8 px-4 py-8 sm:px-6">
      <div>
        <Badge variant="secondary" className="gap-1.5">
          <ClipboardList className="h-3.5 w-3.5 text-primary" />
          Testovací modul
        </Badge>
        <h1 className="mt-2 text-3xl font-bold tracking-tight">
          Konfigurátor testov &amp; Testovací Engine
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Zostavte si cvičný test na mieru podľa okruhov, počtu otázok a vašej
          doterajšej úspešnosti.
        </p>
      </div>

      <TestSuite
        subjectGroups={subjectGroups}
        initialSelectedCategoryIds={initialSelectedCategoryIds}
        initialFilterMode={initialFilterMode}
      />
    </main>
  );
}
