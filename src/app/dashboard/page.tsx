import Link from "next/link";
import { redirect } from "next/navigation";
import { createClient } from "@/utils/supabase/server";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Progress,
  getAccuracyColorClasses,
} from "@/components/ui/progress";
import {
  Activity,
  AlertTriangle,
  ArrowRight,
  BarChart3,
  BookOpen,
  CheckCircle2,
  ClipboardList,
  Flame,
  Layers,
  Target,
  Trophy,
} from "lucide-react";

export const dynamic = "force-dynamic";

interface CategoryAnalytics {
  id: string;
  name: string;
  subjectId: string;
  totalQuestionsInDb: number;
  answeredCount: number;
  correctCount: number;
  accuracy: number | null; // null ak študent v kategórii ešte nič nezodpovedal
}

interface SubjectAnalytics {
  id: string;
  name: string;
  answeredCount: number;
  correctCount: number;
  accuracy: number | null;
  categories: CategoryAnalytics[];
}

/**
 * Odhad počtu vyriešených testov / relácií:
 * Keďže pri vyhodnotení testu sa všetky odpovede uložia naraz s rovnakým/blízkym
 * časom `created_at`, zoskupíme záznamy v `user_progress`, ktoré sú od seba
 * vzdialené viac ako 60 sekúnd, ako samostatné testovacie relácie.
 */
function countCompletedTestSessions(timestamps: string[]): number {
  if (timestamps.length === 0) return 0;
  const sortedMs = timestamps
    .map((ts) => new Date(ts).getTime())
    .filter((ms) => !Number.isNaN(ms))
    .sort((a, b) => a - b);

  if (sortedMs.length === 0) return 0;

  let sessions = 1;
  for (let i = 1; i < sortedMs.length; i++) {
    if (sortedMs[i] - sortedMs[i - 1] > 60_000) {
      sessions++;
    }
  }
  return sessions;
}

export default async function DashboardPage() {
  const supabase = createClient();

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    redirect("/login?next=/dashboard");
  }

  // 1. Dátová agregácia zo Supabase
  const [
    { data: subjects },
    { data: categories },
    { data: questions },
    { data: progressRows },
  ] = await Promise.all([
    supabase.from("subjects").select("id, name").order("name"),
    supabase.from("categories").select("id, subject_id, name").order("name"),
    supabase.from("questions").select("id, category_id"),
    supabase
      .from("user_progress")
      .select("id, question_id, is_correct, created_at")
      .eq("user_id", user.id)
      .order("created_at", { ascending: false }),
  ]);

  const safeSubjects = subjects ?? [];
  const safeCategories = categories ?? [];
  const safeQuestions = questions ?? [];
  const safeProgress = progressRows ?? [];

  // Mapovanie question_id -> category_id
  const questionToCategoryMap = new Map<string, string>();
  const questionsCountByCategory = new Map<string, number>();

  for (const q of safeQuestions) {
    questionToCategoryMap.set(q.id, q.category_id);
    questionsCountByCategory.set(
      q.category_id,
      (questionsCountByCategory.get(q.category_id) ?? 0) + 1
    );
  }

  // Agregácia odpovedí podľa category_id
  const statsByCategory = new Map<
    string,
    { answered: number; correct: number }
  >();

  let totalAnswered = 0;
  let totalCorrect = 0;

  for (const row of safeProgress) {
    totalAnswered++;
    if (row.is_correct) {
      totalCorrect++;
    }

    const catId = questionToCategoryMap.get(row.question_id);
    if (!catId) continue;

    const current = statsByCategory.get(catId) ?? { answered: 0, correct: 0 };
    current.answered += 1;
    if (row.is_correct) {
      current.correct += 1;
    }
    statsByCategory.set(catId, current);
  }

  const overallAccuracy =
    totalAnswered > 0 ? Math.round((totalCorrect / totalAnswered) * 100) : 0;

  const completedTestsCount = countCompletedTestSessions(
    safeProgress.map((p) => p.created_at)
  );

  // Zostavenie analytiky pre predmety a podkategórie
  const subjectAnalytics: SubjectAnalytics[] = safeSubjects.map((subj) => {
    const subjCategories: CategoryAnalytics[] = safeCategories
      .filter((c) => c.subject_id === subj.id)
      .map((cat) => {
        const stat = statsByCategory.get(cat.id) ?? {
          answered: 0,
          correct: 0,
        };
        const accuracy =
          stat.answered > 0
            ? Math.round((stat.correct / stat.answered) * 100)
            : null;

        return {
          id: cat.id,
          name: cat.name,
          subjectId: subj.id,
          totalQuestionsInDb: questionsCountByCategory.get(cat.id) ?? 0,
          answeredCount: stat.answered,
          correctCount: stat.correct,
          accuracy,
        };
      });

    const subjAnswered = subjCategories.reduce(
      (sum, c) => sum + c.answeredCount,
      0
    );
    const subjCorrect = subjCategories.reduce(
      (sum, c) => sum + c.correctCount,
      0
    );
    const subjAccuracy =
      subjAnswered > 0 ? Math.round((subjCorrect / subjAnswered) * 100) : null;

    return {
      id: subj.id,
      name: subj.name,
      answeredCount: subjAnswered,
      correctCount: subjCorrect,
      accuracy: subjAccuracy,
      categories: subjCategories,
    };
  });

  // Identifikácia "Slabých miest": kategórie, v ktorých má študent úspešnosť < 65 %
  const weakCategories = subjectAnalytics
    .flatMap((s) => s.categories)
    .filter((cat) => cat.accuracy !== null && cat.accuracy < 65);

  const weakCategoryIds = weakCategories.map((c) => c.id);

  // URL pre tlačidlo "Precvičiť slabé miesta"
  const weakSpotsHref =
    weakCategoryIds.length > 0
      ? `/test?categories=${encodeURIComponent(
          weakCategoryIds.join(",")
        )}&filter=incorrect`
      : `/test?filter=incorrect`;

  const overallColors = getAccuracyColorClasses(overallAccuracy);

  return (
    <main className="mx-auto max-w-6xl space-y-6 px-3.5 py-6 sm:space-y-8 sm:px-6 sm:py-8">
      {/* Hlavička Dashboardu */}
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <Badge variant="secondary" className="gap-1.5">
            <BarChart3 className="h-3.5 w-3.5 text-primary" />
            Študentský Dashboard &amp; Analytika
          </Badge>
          <h1 className="mt-2 text-2xl font-bold tracking-tight sm:text-3xl">
            Prehľad vašej prípravy
          </h1>
          <p className="mt-1 truncate text-xs text-muted-foreground sm:text-sm">
            Prihlásený účet:{" "}
            <strong className="text-foreground">{user.email}</strong>
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2.5 sm:gap-3">
          <Button asChild variant="outline" className="w-full sm:w-auto">
            <Link href="/test">
              <ClipboardList className="h-4 w-4" />
              Vlastný test s časovačom
            </Link>
          </Button>
        </div>
      </div>

      {/* 3. Akcia "Slabé miesta" - Veľký CTA panel */}
      <Card className="border-2 border-primary/25 bg-gradient-to-r from-primary/5 via-background to-amber-500/5 shadow-sm">
        <CardContent className="flex flex-col items-start justify-between gap-6 p-6 sm:p-8 lg:flex-row lg:items-center">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 rounded-full bg-amber-500/10 px-3 py-1 text-xs font-semibold text-amber-700">
              <Flame className="h-4 w-4 text-amber-600" />
              Cielené zlepšovanie výsledkov
            </div>
            <h2 className="text-2xl font-bold tracking-tight">
              Zamerajte sa na svoje slabé miesta
            </h2>
            <p className="max-w-2xl text-sm text-muted-foreground">
              {weakCategories.length > 0 ? (
                <>
                  Máte <strong>{weakCategories.length}</strong>{" "}
                  {weakCategories.length === 1
                    ? "kategóriu"
                    : weakCategories.length <= 4
                      ? "kategórie"
                      : "kategórií"}{" "}
                  s úspešnosťou pod <strong>65 %</strong> (
                  {weakCategories.map((c) => c.name).join(", ")}). Kliknutím
                  nižšie sa otvorí Konfigurátor testov s automaticky
                  predvybranými slabými kategóriami a filtrom{" "}
                  <strong>„Iba nesprávne zodpovedané“</strong>.
                </>
              ) : totalAnswered > 0 ? (
                <>
                  Skvelá práca! Momentálne nemáte žiadnu kategóriu s
                  úspešnosťou pod 65 %. Stále si však môžete precvičiť svoje
                  doteraz nesprávne zodpovedané otázky.
                </>
              ) : (
                <>
                  Zatiaľ ste nevyriešili žiadne otázky. Po vyriešení prvých
                  testov vám tu systém automaticky vyfiltruje kategórie s
                  úspešnosťou pod 65 %.
                </>
              )}
            </p>
          </div>

          <Button
            asChild
            size="lg"
            className="w-full shrink-0 gap-2 text-base font-semibold shadow-md sm:w-auto"
          >
            <Link href={weakSpotsHref}>
              <Target className="h-5 w-5" />
              Precvičiť slabé miesta
              <ArrowRight className="h-4 w-4" />
            </Link>
          </Button>
        </CardContent>
      </Card>

      {/* 2. UI Štatistiky: 3 hlavné metriky */}
      <section className="grid gap-4 sm:grid-cols-3">
        {/* Metrika 1: Celkový počet vyriešených testov / otázok */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Vyriešené testy / otázky
            </CardTitle>
            <BookOpen className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent className="space-y-1">
            <div className="text-3xl font-bold">
              {completedTestsCount}{" "}
              <span className="text-lg font-normal text-muted-foreground">
                testov
              </span>{" "}
              / {totalAnswered}{" "}
              <span className="text-lg font-normal text-muted-foreground">
                otázok
              </span>
            </div>
            <p className="text-xs text-muted-foreground">
              Z toho {totalCorrect} správnych a {totalAnswered - totalCorrect}{" "}
              nesprávnych odpovedí
            </p>
          </CardContent>
        </Card>

        {/* Metrika 2: Celková priemerná úspešnosť v percentách */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Celková priemerná úspešnosť
            </CardTitle>
            <Trophy className="h-4 w-4 text-amber-500" />
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex items-baseline justify-between">
              <span
                className={`text-3xl font-bold ${
                  totalAnswered > 0 ? overallColors.text : "text-foreground"
                }`}
              >
                {overallAccuracy} %
              </span>
              <span className="text-xs text-muted-foreground">
                Cieľ na prijímačky: 80+ %
              </span>
            </div>
            <Progress
              value={overallAccuracy}
              indicatorClassName={
                totalAnswered > 0 ? overallColors.bar : "bg-muted-foreground/30"
              }
            />
          </CardContent>
        </Card>

        {/* Metrika 3: Kategórie vyžadujúce pozornosť (< 65 %) */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Slabé kategórie (&lt; 65 %)
            </CardTitle>
            {weakCategories.length > 0 ? (
              <AlertTriangle className="h-4 w-4 text-red-500" />
            ) : (
              <CheckCircle2 className="h-4 w-4 text-emerald-600" />
            )}
          </CardHeader>
          <CardContent className="space-y-1">
            <div className="text-3xl font-bold">{weakCategories.length}</div>
            <p className="text-xs text-muted-foreground">
              {weakCategories.length > 0
                ? "Odporúčame precvičiť cez tlačidlo vyššie"
                : "Žiadna kategória nie je pod hranicou 65 %"}
            </p>
          </CardContent>
        </Card>
      </section>

      {/* Zoznam predmetov a podkategórií s ich špecifickou úspešnosťou a progress barmi */}
      <section className="space-y-5">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div>
            <h2 className="text-xl font-bold tracking-tight">
              Úspešnosť podľa predmetov a kategórií
            </h2>
            <p className="text-sm text-muted-foreground">
              Farebná škála progress barov:{" "}
              <span className="font-medium text-red-600">
                červená (&lt; 60 %)
              </span>
              ,{" "}
              <span className="font-medium text-amber-600">
                oranžová (60 % – 80 %)
              </span>
              ,{" "}
              <span className="font-medium text-emerald-600">
                zelená (&gt; 80 %)
              </span>
              .
            </p>
          </div>
        </div>

        {subjectAnalytics.length === 0 ? (
          <Card>
            <CardHeader>
              <CardTitle>Zatiaľ nie sú vytvorené žiadne predmety</CardTitle>
              <CardDescription>
                Naimportujte otázky cez administrátorskú sekciu{" "}
                <Link href="/admin" className="text-primary underline">
                  /admin
                </Link>
                .
              </CardDescription>
            </CardHeader>
          </Card>
        ) : (
          <div className="grid gap-6">
            {subjectAnalytics.map((subject) => {
              const subjAcc = subject.accuracy ?? 0;
              const subjColors = getAccuracyColorClasses(subjAcc);

              return (
                <Card key={subject.id} className="overflow-hidden">
                  <CardHeader className="border-b bg-muted/20">
                    <div className="flex flex-wrap items-center justify-between gap-4">
                      <div className="flex items-center gap-3">
                        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
                          <Activity className="h-5 w-5" />
                        </div>
                        <div>
                          <CardTitle className="text-xl">
                            {subject.name}
                          </CardTitle>
                          <CardDescription>
                            Zodpovedané: {subject.answeredCount} otázok (správne:{" "}
                            {subject.correctCount})
                          </CardDescription>
                        </div>
                      </div>

                      <div className="flex items-center gap-3">
                        {subject.accuracy !== null ? (
                          <span
                            className={`rounded-full border px-3 py-1 text-sm font-bold ${subjColors.badge}`}
                          >
                            Priemer predmetu: {subject.accuracy} %
                          </span>
                        ) : (
                          <Badge variant="outline">Zatiaľ neriešené</Badge>
                        )}
                      </div>
                    </div>

                    {subject.accuracy !== null && (
                      <div className="pt-2">
                        <Progress
                          value={subject.accuracy}
                          indicatorClassName={subjColors.bar}
                          className="h-2"
                        />
                      </div>
                    )}
                  </CardHeader>

                  <CardContent className="divide-y p-0">
                    {subject.categories.length === 0 ? (
                      <div className="p-6 text-sm text-muted-foreground">
                        Tento predmet zatiaľ neobsahuje žiadne podkategórie.
                      </div>
                    ) : (
                      subject.categories.map((cat) => {
                        const hasAttempts = cat.accuracy !== null;
                        const accValue = cat.accuracy ?? 0;
                        const catColors = getAccuracyColorClasses(accValue);
                        const isWeak = hasAttempts && accValue < 65;

                        return (
                          <div
                            key={cat.id}
                            className="flex flex-col gap-3 p-4 sm:flex-row sm:items-center sm:justify-between sm:px-6"
                          >
                            <div className="space-y-1 sm:max-w-md">
                              <div className="flex flex-wrap items-center gap-2">
                                <Layers className="h-4 w-4 text-muted-foreground" />
                                <span className="font-medium text-foreground">
                                  {cat.name}
                                </span>
                                {isWeak && (
                                  <Badge
                                    variant="destructive"
                                    className="text-[11px] px-2 py-0"
                                  >
                                    Slabé miesto (&lt; 65 %)
                                  </Badge>
                                )}
                              </div>
                              <p className="text-xs text-muted-foreground">
                                Zodpovedaných pokusov: {cat.answeredCount} (
                                {cat.correctCount} správne) • Otázok v banke:{" "}
                                {cat.totalQuestionsInDb}
                              </p>
                            </div>

                            <div className="flex flex-1 flex-col gap-1.5 sm:max-w-xs">
                              <div className="flex items-center justify-between text-xs">
                                <span className="text-muted-foreground">
                                  Úspešnosť okruhu
                                </span>
                                {hasAttempts ? (
                                  <span
                                    className={`font-bold ${catColors.text}`}
                                  >
                                    {accValue} %
                                  </span>
                                ) : (
                                  <span className="text-muted-foreground">
                                    0 pokusov
                                  </span>
                                )}
                              </div>

                              <Progress
                                value={hasAttempts ? accValue : 0}
                                indicatorClassName={
                                  hasAttempts
                                    ? catColors.bar
                                    : "bg-muted-foreground/20"
                                }
                              />
                            </div>

                              <div className="w-full shrink-0 sm:w-auto">
                              <Button
                                asChild
                                variant="outline"
                                size="sm"
                                className="w-full sm:w-auto sm:variant-ghost"
                              >
                                <Link href={`/test?categories=${cat.id}`}>
                                  Precvičiť
                                  <ArrowRight className="h-3.5 w-3.5" />
                                </Link>
                              </Button>
                            </div>
                          </div>
                        );
                      })
                    )}
                  </CardContent>
                </Card>
              );
            })}
          </div>
        )}
      </section>
    </main>
  );
}

