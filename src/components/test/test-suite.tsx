"use client";

import * as React from "react";
import {
  evaluateSingleQuestionAction,
  evaluateTestAction,
  generateTestQuestionsAction,
  type ActiveTestQuestion,
  type EvaluatedQuestionResult,
  type QuestionFilterMode,
  type QuestionOrderMode,
  type TestEvaluationSummary,
} from "@/app/test/actions";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import {
  AlertCircle,
  ArrowLeft,
  ArrowRight,
  BookOpen,
  CheckCheck,
  CheckCircle2,
  ClipboardCheck,
  Clock,
  Filter,
  GraduationCap,
  Hash,
  HelpCircle,
  Layers,
  ListOrdered,
  Loader2,
  Pause,
  Play,
  RotateCcw,
  Shuffle,
  Sparkles,
  Timer,
  Trophy,
  XCircle,
  Zap,
} from "lucide-react";

export interface CategoryWithCount {
  id: string;
  subject_id: string;
  name: string;
  questionCount: number;
}

export interface SubjectGroup {
  id: string;
  name: string;
  categories: CategoryWithCount[];
}

interface TestSuiteProps {
  subjectGroups: SubjectGroup[];
  initialSelectedCategoryIds?: string[];
  initialFilterMode?: QuestionFilterMode;
}

export type TestMode = "training" | "exam";

const QUESTION_COUNT_OPTIONS = [10, 20, 30, 50, 100] as const;

const TIME_LIMIT_OPTIONS: {
  minutes: number;
  label: string;
  sublabel: string;
}[] = [
  { minutes: 0, label: "Bez limitu", sublabel: "Stopky" },
  { minutes: 10, label: "10 min", sublabel: "Rýchly test" },
  { minutes: 20, label: "20 min", sublabel: "Štandard" },
  { minutes: 45, label: "45 min", sublabel: "Dlhší test" },
  { minutes: 60, label: "60 min", sublabel: "Prijímačky 50Q" },
  { minutes: 90, label: "90 min", sublabel: "Prijímačky 100Q" },
];

const FILTER_OPTIONS: {
  value: QuestionFilterMode;
  label: string;
  description: string;
}[] = [
  {
    value: "all",
    label: "Všetky",
    description: "Náhodný výber zo všetkých otázok vo zvolených kategóriách.",
  },
  {
    value: "incorrect",
    label: "Iba nesprávne zodpovedané",
    description:
      "Otázky z tabuľky user_progress, na ktoré ste naposledy odpovedali nesprávne.",
  },
  {
    value: "unseen",
    label: "Nové (ešte nevidené)",
    description:
      "Otázky, ktoré ešte nemajú žiadny záznam vo vašej histórii user_progress.",
  },
];

function formatSecondsToMMSS(totalSeconds: number): string {
  const safe = Math.max(0, Math.floor(totalSeconds));
  const hours = Math.floor(safe / 3600);
  const minutes = Math.floor((safe % 3600) / 60);
  const seconds = safe % 60;

  const mm = String(minutes).padStart(2, "0");
  const ss = String(seconds).padStart(2, "0");

  if (hours > 0) {
    return `${hours}:${mm}:${ss}`;
  }
  return `${mm}:${ss}`;
}

export function TestSuite({
  subjectGroups,
  initialSelectedCategoryIds,
  initialFilterMode,
}: TestSuiteProps) {
  const allCategoryIds = React.useMemo(
    () =>
      subjectGroups.flatMap((group) => group.categories.map((cat) => cat.id)),
    [subjectGroups]
  );

  // ==========================================================================
  // STAV KONFIGURÁTORA (TEST BUILDER)
  // ==========================================================================
  const [selectedCategoryIds, setSelectedCategoryIds] = React.useState<
    string[]
  >(() =>
    initialSelectedCategoryIds && initialSelectedCategoryIds.length > 0
      ? initialSelectedCategoryIds
      : allCategoryIds
  );
  const [questionCount, setQuestionCount] = React.useState<number>(10);
  const [timeLimitMinutes, setTimeLimitMinutes] = React.useState<number>(15);
  const [filterMode, setFilterMode] = React.useState<QuestionFilterMode>(
    initialFilterMode ?? "all"
  );
  const [orderMode, setOrderMode] = React.useState<QuestionOrderMode>("random");
  const [startQuestionNumber, setStartQuestionNumber] = React.useState<number>(1);
  const [testMode, setTestMode] = React.useState<TestMode>("training");

  // Nastavenie odporúčaného času pri zmene počtu otázok (ak používateľ nezvolil Bez limitu)
  function handleQuestionCountSelect(count: number) {
    setQuestionCount(count);
    if (timeLimitMinutes > 0) {
      if (count <= 10) setTimeLimitMinutes(10);
      else if (count <= 20) setTimeLimitMinutes(20);
      else if (count <= 30) setTimeLimitMinutes(30);
      else if (count <= 50) setTimeLimitMinutes(45);
      else if (count <= 100) setTimeLimitMinutes(90);
      else setTimeLimitMinutes(60);
    }
  }

  // ==========================================================================
  // STAV TESTOVACIEHO ENGINU, ČASOVAČA A VYHODNOTENIA
  // ==========================================================================
  const [stage, setStage] = React.useState<"builder" | "running" | "results">(
    "builder"
  );
  const [activeQuestions, setActiveQuestions] = React.useState<
    ActiveTestQuestion[]
  >([]);
  const [currentIndex, setCurrentIndex] = React.useState<number>(0);
  const [answersMap, setAnswersMap] = React.useState<Record<string, string[]>>(
    {}
  );
  const [evaluatedQuestionsMap, setEvaluatedQuestionsMap] = React.useState<
    Record<string, EvaluatedQuestionResult>
  >({});
  const [isEvaluatingSingle, setIsEvaluatingSingle] = React.useState(false);
  const [evaluation, setEvaluation] =
    React.useState<TestEvaluationSummary | null>(null);

  // Časovač (v sekundách)
  const [elapsedSeconds, setElapsedSeconds] = React.useState<number>(0);
  const [remainingSeconds, setRemainingSeconds] = React.useState<number | null>(
    null
  );
  const [isTimerPaused, setIsTimerPaused] = React.useState<boolean>(false);
  const [timedOut, setTimedOut] = React.useState<boolean>(false);

  const [isLoading, setIsLoading] = React.useState(false);
  const [errorMessage, setErrorMessage] = React.useState<string | null>(null);

  // Ref pre automatické odoslanie pri vypršaní časovača
  const autoSubmitTriggeredRef = React.useRef(false);

  const categoryMetaMap = React.useMemo(() => {
    const map = new Map<string, { categoryName: string; subjectName: string }>();
    for (const group of subjectGroups) {
      for (const cat of group.categories) {
        map.set(cat.id, {
          categoryName: cat.name,
          subjectName: group.name,
        });
      }
    }
    return map;
  }, [subjectGroups]);

  // Prepínanie jednej kategórie v Konfigurátore
  function toggleCategory(categoryId: string) {
    setSelectedCategoryIds((prev) =>
      prev.includes(categoryId)
        ? prev.filter((id) => id !== categoryId)
        : [...prev, categoryId]
    );
  }

  // Prepínanie všetkých kategórií v rámci jedného predmetu
  function toggleSubjectCategories(subjectCategoryIds: string[]) {
    const allSelected = subjectCategoryIds.every((id) =>
      selectedCategoryIds.includes(id)
    );
    if (allSelected) {
      setSelectedCategoryIds((prev) =>
        prev.filter((id) => !subjectCategoryIds.includes(id))
      );
    } else {
      setSelectedCategoryIds((prev) =>
        Array.from(new Set([...prev, ...subjectCategoryIds]))
      );
    }
  }

  // Okamžité vyhodnotenie jednej otázky (režim po jednej otázke)
  async function handleEvaluateSingleQuestion(questionId: string) {
    if (isEvaluatingSingle || isTimerPaused) return;
    const selected = answersMap[questionId] ?? [];
    setIsEvaluatingSingle(true);
    setErrorMessage(null);
    try {
      const response = await evaluateSingleQuestionAction(questionId, selected);
      if (response.error || !response.result) {
        setErrorMessage(response.error ?? "Nepodarilo sa vyhodnotiť otázku.");
        return;
      }
      setEvaluatedQuestionsMap((prev) => ({
        ...prev,
        [questionId]: response.result!,
      }));
    } finally {
      setIsEvaluatingSingle(false);
    }
  }

  // Odoslanie celého testu na vyhodnotenie a uloženie do user_progress
  const submitTestEvaluation = React.useCallback(
    async (isTimeout = false) => {
      if (isLoading) return;
      setErrorMessage(null);
      setIsLoading(true);
      if (isTimeout) {
        setTimedOut(true);
      }

      try {
        const unEvaluatedQuestions = activeQuestions.filter(
          (q) => !evaluatedQuestionsMap[q.id]
        );

        const finalResultsMap: Record<string, EvaluatedQuestionResult> = {
          ...evaluatedQuestionsMap,
        };

        if (unEvaluatedQuestions.length > 0) {
          const submissions = unEvaluatedQuestions.map((q) => ({
            questionId: q.id,
            selectedOptionIds: answersMap[q.id] ?? [],
          }));

          const response = await evaluateTestAction(submissions);

          if (response.error || !response.evaluation) {
            setErrorMessage(response.error ?? "Nepodarilo sa vyhodnotiť test.");
            autoSubmitTriggeredRef.current = false;
            return;
          }

          for (const res of response.evaluation.results) {
            finalResultsMap[res.questionId] = res;
          }
        }

        const finalResults = activeQuestions
          .map((q) => finalResultsMap[q.id])
          .filter(Boolean);

        const correctCount = finalResults.filter((r) => r.isCorrect).length;
        const totalQuestions = finalResults.length;
        const scorePercentage =
          totalQuestions > 0
            ? Math.round((correctCount / totalQuestions) * 100)
            : 0;

        setEvaluation({
          totalQuestions,
          correctCount,
          scorePercentage,
          results: finalResults,
        });
        setStage("results");
        window.scrollTo({ top: 0, behavior: "smooth" });
      } finally {
        setIsLoading(false);
      }
    },
    [activeQuestions, answersMap, evaluatedQuestionsMap, isLoading]
  );

  // Interval časovača počas behu testu
  React.useEffect(() => {
    if (stage !== "running" || isTimerPaused || isLoading) {
      return;
    }

    const interval = window.setInterval(() => {
      setElapsedSeconds((prev) => prev + 1);

      if (timeLimitMinutes > 0) {
        setRemainingSeconds((prev) => {
          if (prev === null) return null;
          if (prev <= 1) {
            return 0;
          }
          return prev - 1;
        });
      }
    }, 1000);

    return () => window.clearInterval(interval);
  }, [stage, isTimerPaused, isLoading, timeLimitMinutes]);

  // Automatické vyhodnotenie pri dosiahnutí 00:00
  React.useEffect(() => {
    if (
      stage === "running" &&
      timeLimitMinutes > 0 &&
      remainingSeconds === 0 &&
      !autoSubmitTriggeredRef.current
    ) {
      autoSubmitTriggeredRef.current = true;
      void submitTestEvaluation(true);
    }
  }, [stage, timeLimitMinutes, remainingSeconds, submitTestEvaluation]);

  // Spustenie testu
  async function handleStartTest(event: React.FormEvent) {
    event.preventDefault();
    setErrorMessage(null);

    if (selectedCategoryIds.length === 0) {
      setErrorMessage("Zaškrtnite prosím aspoň jednu kategóriu otázok.");
      return;
    }

    setIsLoading(true);
    try {
      const response = await generateTestQuestionsAction({
        categoryIds: selectedCategoryIds,
        questionCount,
        filterMode,
        orderMode,
        startQuestionNumber:
          orderMode === "sequential" ? startQuestionNumber : undefined,
      });

      if (response.error || !response.questions) {
        setErrorMessage(
          response.error ?? "Nepodarilo sa načítať otázky pre test."
        );
        return;
      }

      autoSubmitTriggeredRef.current = false;
      setTimedOut(false);
      setElapsedSeconds(0);
      setIsTimerPaused(false);
      setRemainingSeconds(
        timeLimitMinutes > 0 ? timeLimitMinutes * 60 : null
      );

      setActiveQuestions(response.questions);
      setAnswersMap({});
      setEvaluatedQuestionsMap({});
      setCurrentIndex(0);
      setEvaluation(null);
      setStage("running");
      window.scrollTo({ top: 0, behavior: "smooth" });
    } finally {
      setIsLoading(false);
    }
  }

  // Výber odpovede počas testu
  function handleOptionChange(
    questionId: string,
    optionId: string,
    isMultipleChoice: boolean
  ) {
    if (isTimerPaused) return;

    setAnswersMap((prev) => {
      const currentSelected = prev[questionId] ?? [];
      if (isMultipleChoice) {
        const exists = currentSelected.includes(optionId);
        const updated = exists
          ? currentSelected.filter((id) => id !== optionId)
          : [...currentSelected, optionId];
        return { ...prev, [questionId]: updated };
      } else {
        return { ...prev, [questionId]: [optionId] };
      }
    });
  }

  function handleResetToBuilder() {
    setStage("builder");
    setActiveQuestions([]);
    setAnswersMap({});
    setEvaluatedQuestionsMap({});
    setCurrentIndex(0);
    setEvaluation(null);
    setErrorMessage(null);
    setTimedOut(false);
  }

  // ==========================================================================
  // 1. OBRAZOVKA: KONFIGURÁTOR TESTU (TEST BUILDER)
  // ==========================================================================
  if (stage === "builder") {
    return (
      <form onSubmit={handleStartTest} className="space-y-6 pb-8">
        {errorMessage && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Upozornenie</AlertTitle>
            <AlertDescription>{errorMessage}</AlertDescription>
          </Alert>
        )}

        {/* Krok 1: Výber režimu (Trénovací vs Testovací) */}
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-primary shrink-0" />
            <h2 className="text-base sm:text-lg font-bold">1. Zvoľte režim</h2>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            <button
              type="button"
              onClick={() => setTestMode("training")}
              className={`flex items-start gap-3.5 rounded-2xl border p-4 sm:p-5 text-left transition-all active:scale-[0.99] ${
                testMode === "training"
                  ? "border-primary bg-primary/5 ring-2 ring-primary shadow-sm"
                  : "border-border bg-card hover:bg-accent/40"
              }`}
            >
              <div
                className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-xl ${
                  testMode === "training"
                    ? "bg-primary text-primary-foreground shadow-sm"
                    : "bg-muted text-muted-foreground"
                }`}
              >
                <GraduationCap className="h-6 w-6" />
              </div>
              <div className="space-y-1">
                <div className="flex items-center gap-2 font-bold text-base sm:text-lg">
                  <span>Trénovací režim</span>
                  {testMode === "training" && (
                    <Badge className="bg-primary text-primary-foreground text-xs py-0.5 px-2">
                      Zvolené
                    </Badge>
                  )}
                </div>
                <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
                  Ideálne na učenie. Po označení odpovedí sa vám otázka ihneď vyhodnotí, keď pôjdete na ďalšiu otázku, aby ste videli správne odpovede aj oficiálne vysvetlenie.
                </p>
              </div>
            </button>

            <button
              type="button"
              onClick={() => setTestMode("exam")}
              className={`flex items-start gap-3.5 rounded-2xl border p-4 sm:p-5 text-left transition-all active:scale-[0.99] ${
                testMode === "exam"
                  ? "border-primary bg-primary/5 ring-2 ring-primary shadow-sm"
                  : "border-border bg-card hover:bg-accent/40"
              }`}
            >
              <div
                className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-xl ${
                  testMode === "exam"
                    ? "bg-primary text-primary-foreground shadow-sm"
                    : "bg-muted text-muted-foreground"
                }`}
              >
                <ClipboardCheck className="h-6 w-6" />
              </div>
              <div className="space-y-1">
                <div className="flex items-center gap-2 font-bold text-base sm:text-lg">
                  <span>Testovací režim</span>
                  {testMode === "exam" && (
                    <Badge className="bg-primary text-primary-foreground text-xs py-0.5 px-2">
                      Zvolené
                    </Badge>
                  )}
                </div>
                <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
                  Reálna simulácia prijímačiek. Počas testu sa odpovede nezobrazujú – kompletné detailné vyhodnotenie a percento úspešnosti uvidíte až úplne na konci testu.
                </p>
              </div>
            </button>
          </div>
        </div>

        {/* Krok 2: Výber kategórií */}
        <Card>
          <CardHeader className="p-4 sm:p-6">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <CardTitle className="flex items-center gap-2 text-base sm:text-lg">
                  <Layers className="h-5 w-5 shrink-0 text-primary" />
                  2. Vyberte kategórie otázok
                </CardTitle>
                <CardDescription className="mt-1 text-xs sm:text-sm">
                  Zaškrtnite tematické okruhy, z ktorých chcete zostaviť test.
                </CardDescription>
              </div>

              <div className="flex items-center gap-2">
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  className="flex-1 sm:flex-none"
                  onClick={() => setSelectedCategoryIds(allCategoryIds)}
                >
                  <CheckCheck className="h-4 w-4" />
                  Vybrať všetky
                </Button>
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="flex-1 sm:flex-none"
                  onClick={() => setSelectedCategoryIds([])}
                >
                  Zrušiť výber
                </Button>
              </div>
            </div>
          </CardHeader>

          <CardContent className="space-y-4 p-4 pt-0 sm:space-y-6 sm:p-6 sm:pt-0">
            {subjectGroups.length === 0 ? (
              <div className="rounded-lg border border-dashed p-6 text-center text-sm text-muted-foreground">
                V databáze sa zatiaľ nenachádzajú žiadne kategórie ani otázky.
                Naimportujte ich v sekcii <code>/admin</code>.
              </div>
            ) : (
              subjectGroups.map((subject) => {
                const subjectCatIds = subject.categories.map((c) => c.id);
                const allInSubjectSelected =
                  subjectCatIds.length > 0 &&
                  subjectCatIds.every((id) => selectedCategoryIds.includes(id));

                return (
                  <div
                    key={subject.id}
                    className="space-y-3 rounded-xl border bg-muted/20 p-3.5 sm:p-4"
                  >
                    <div className="flex flex-wrap items-center justify-between gap-2 border-b pb-2.5">
                      <div className="flex items-center gap-2 font-semibold">
                        <BookOpen className="h-4 w-4 shrink-0 text-primary" />
                        <span className="text-sm sm:text-base">
                          {subject.name}
                        </span>
                        <Badge variant="secondary" className="text-xs">
                          {subject.categories.length} okruhov
                        </Badge>
                      </div>

                      {subject.categories.length > 0 && (
                        <button
                          type="button"
                          onClick={() =>
                            toggleSubjectCategories(subjectCatIds)
                          }
                          className="text-xs font-medium text-primary hover:underline"
                        >
                          {allInSubjectSelected
                            ? "Odznačiť predmet"
                            : "Označiť celý predmet"}
                        </button>
                      )}
                    </div>

                    <div className="grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-3">
                      {subject.categories.map((cat) => {
                        const isChecked = selectedCategoryIds.includes(cat.id);
                        return (
                          <label
                            key={cat.id}
                            className={`flex min-h-[48px] cursor-pointer touch-manipulation items-center justify-between gap-3 rounded-lg border p-3 text-sm transition-colors active:scale-[0.99] ${
                              isChecked
                                ? "border-primary bg-primary/5 font-medium"
                                : "border-border bg-background hover:bg-accent/50"
                            }`}
                          >
                            <div className="flex min-w-0 items-center gap-2.5">
                              <input
                                type="checkbox"
                                checked={isChecked}
                                onChange={() => toggleCategory(cat.id)}
                                className="h-4 w-4 shrink-0 rounded border-input text-primary focus:ring-primary"
                              />
                              <span className="truncate">{cat.name}</span>
                            </div>
                            <Badge variant="outline" className="shrink-0">
                              {cat.questionCount}
                            </Badge>
                          </label>
                        );
                      })}
                    </div>
                  </div>
                );
              })
            )}
          </CardContent>
        </Card>

        {/* Krok 2 a 3: Počet otázok a Časovač */}
        <div className="grid gap-6 md:grid-cols-2">
          {/* Krok 2: Spôsob výberu a Počet otázok */}
          <Card>
            <CardHeader className="p-4 sm:p-6">
              <CardTitle className="flex items-center gap-2 text-base sm:text-lg">
                <HelpCircle className="h-5 w-5 shrink-0 text-primary" />
                3. Spôsob výberu a počet otázok
              </CardTitle>
              <CardDescription className="text-xs sm:text-sm">
                Zvoľte náhodné premiešanie alebo precvičovanie konkrétneho rozsahu z testovnice.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4 p-4 pt-0 sm:p-6 sm:pt-0">
              {/* Prepínač: Náhodný výber vs. Od konkrétnej otázky */}
              <div className="grid grid-cols-2 gap-2 rounded-xl bg-muted/40 p-1">
                <button
                  type="button"
                  onClick={() => setOrderMode("random")}
                  className={`flex items-center justify-center gap-2 rounded-lg py-2 text-xs font-semibold sm:text-sm transition-all ${
                    orderMode === "random"
                      ? "bg-background text-foreground shadow-sm ring-1 ring-border"
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  <Shuffle className="h-4 w-4 shrink-0 text-primary" />
                  <span>Náhodný výber</span>
                </button>
                <button
                  type="button"
                  onClick={() => setOrderMode("sequential")}
                  className={`flex items-center justify-center gap-2 rounded-lg py-2 text-xs font-semibold sm:text-sm transition-all ${
                    orderMode === "sequential"
                      ? "bg-background text-foreground shadow-sm ring-1 ring-border"
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  <ListOrdered className="h-4 w-4 shrink-0 text-primary" />
                  <span>Od otázky (rozsah)</span>
                </button>
              </div>

              {/* Sekcia: Začať od otázky číslo (zobrazí sa pri sekvenčnom výbere) */}
              {orderMode === "sequential" && (
                <div className="space-y-2.5 rounded-xl border border-primary/25 bg-primary/5 p-3.5 sm:p-4">
                  <div className="flex items-center justify-between gap-3">
                    <label
                      htmlFor="startQInput"
                      className="flex items-center gap-1.5 text-xs font-semibold text-foreground sm:text-sm"
                    >
                      <Hash className="h-4 w-4 text-primary" />
                      Začať od otázky číslo:
                    </label>
                    <input
                      id="startQInput"
                      type="number"
                      min={1}
                      max={1500}
                      value={startQuestionNumber}
                      onChange={(e) => {
                        const val = parseInt(e.target.value, 10);
                        setStartQuestionNumber(
                          isNaN(val) ? 1 : Math.max(1, val)
                        );
                      }}
                      className="w-24 rounded-lg border bg-background px-3 py-1.5 text-right text-base font-bold text-foreground shadow-sm focus:outline-none focus:ring-2 focus:ring-primary"
                    />
                  </div>

                  {/* Rýchle tlačidlá čísel */}
                  <div className="flex flex-wrap items-center gap-1.5 pt-1">
                    <span className="text-[11px] font-medium text-muted-foreground">
                      Rýchly výber:
                    </span>
                    {[1, 50, 100, 150, 200, 250].map((num) => (
                      <button
                        key={num}
                        type="button"
                        onClick={() => setStartQuestionNumber(num)}
                        className={`rounded-md border px-2.5 py-0.5 text-xs font-medium transition-colors ${
                          startQuestionNumber === num
                            ? "border-primary bg-primary text-primary-foreground"
                            : "border-border bg-background text-muted-foreground hover:bg-accent"
                        }`}
                      >
                        č. {num}
                      </button>
                    ))}
                  </div>

                  <div className="rounded-lg bg-background/80 p-2 text-xs text-primary/90 border border-primary/10">
                    Spustí sa test od otázky <strong>č. {startQuestionNumber}</strong> po otázku{" "}
                    <strong>
                      č. {startQuestionNumber + questionCount - 1}
                    </strong>{" "}
                    ({questionCount} otázok v poradí podľa knihy).
                  </div>
                </div>
              )}

              {/* Počet otázok */}
              <div className="space-y-2">
                <span className="text-xs font-semibold text-muted-foreground">
                  Počet otázok:
                </span>
                <div className="grid grid-cols-3 sm:grid-cols-5 gap-2 sm:gap-2.5">
                  {[10, 20, 30, 50, 100].map((count) => {
                    const isSelected = questionCount === count;
                    return (
                      <button
                        key={count}
                        type="button"
                        onClick={() => handleQuestionCountSelect(count)}
                        className={`flex min-h-[58px] touch-manipulation flex-col items-center justify-center rounded-xl border p-2 transition-all active:scale-[0.98] ${
                          isSelected
                            ? "border-primary bg-primary text-primary-foreground shadow-sm"
                            : "border-border bg-background hover:bg-accent"
                        }`}
                      >
                        <span className="text-lg font-bold sm:text-xl">
                          {count}
                        </span>
                        <span
                          className={`text-[11px] ${
                            isSelected
                              ? "text-primary-foreground/80"
                              : "text-muted-foreground"
                          }`}
                        >
                          otázok
                        </span>
                      </button>
                    );
                  })}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Krok 3: Časovač (Časový limit) */}
          <Card>
            <CardHeader className="p-4 sm:p-6">
              <CardTitle className="flex items-center gap-2 text-base sm:text-lg">
                <Timer className="h-5 w-5 shrink-0 text-primary" />
                4. Časovač testu
              </CardTitle>
              <CardDescription className="text-xs sm:text-sm">
                Nastavte si odpočítavanie času ako na prijímačkách alebo režim
                stopiek bez limitu.
              </CardDescription>
            </CardHeader>
            <CardContent className="p-4 pt-0 sm:p-6 sm:pt-0">
              <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 lg:grid-cols-6">
                {TIME_LIMIT_OPTIONS.map((item) => {
                  const isSelected = timeLimitMinutes === item.minutes;
                  return (
                    <button
                      key={item.minutes}
                      type="button"
                      onClick={() => setTimeLimitMinutes(item.minutes)}
                      className={`flex min-h-[68px] touch-manipulation flex-col items-center justify-center rounded-xl border p-2.5 text-center transition-all active:scale-[0.98] ${
                        isSelected
                          ? "border-primary bg-primary text-primary-foreground shadow-sm"
                          : "border-border bg-background hover:bg-accent"
                      }`}
                    >
                      <span className="text-sm font-bold sm:text-base">
                        {item.label}
                      </span>
                      <span
                        className={`mt-0.5 text-[11px] leading-tight ${
                          isSelected
                            ? "text-primary-foreground/85"
                            : "text-muted-foreground"
                        }`}
                      >
                        {item.sublabel}
                      </span>
                    </button>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Krok 5: Filter otázok podľa user_progress */}
        <Card>
          <CardHeader className="p-4 sm:p-6">
            <CardTitle className="flex items-center gap-2 text-base sm:text-lg">
              <Filter className="h-5 w-5 shrink-0 text-primary" />
              5. Filter otázok podľa vašej histórie
            </CardTitle>
            <CardDescription className="text-xs sm:text-sm">
              Filtrovanie otázok na základe vašich predchádzajúcich odpovedí v{" "}
              <code>user_progress</code>.
            </CardDescription>
          </CardHeader>
          <CardContent className="grid gap-2.5 p-4 pt-0 sm:grid-cols-3 sm:p-6 sm:pt-0">
            {FILTER_OPTIONS.map((option) => {
              const isSelected = filterMode === option.value;
              return (
                <label
                  key={option.value}
                  className={`flex cursor-pointer touch-manipulation items-start gap-3 rounded-xl border p-3.5 text-sm transition-colors active:scale-[0.99] ${
                    isSelected
                      ? "border-primary bg-primary/5 ring-1 ring-primary"
                      : "border-border bg-background hover:bg-accent/50"
                  }`}
                >
                  <input
                    type="radio"
                    name="filterMode"
                    value={option.value}
                    checked={isSelected}
                    onChange={() => setFilterMode(option.value)}
                    className="mt-0.5 h-4 w-4 shrink-0 border-input text-primary focus:ring-primary"
                  />
                  <div className="space-y-1">
                    <div className="font-semibold text-foreground">
                      {option.label}
                    </div>
                    <p className="text-xs leading-relaxed text-muted-foreground">
                      {option.description}
                    </p>
                  </div>
                </label>
              );
            })}
          </CardContent>
        </Card>

        {/* Tlačidlo na spustenie testu (responzívne pre mobil aj desktop) */}
        <div className="sticky bottom-3 z-20 flex flex-col gap-3 rounded-xl border bg-card/95 p-4 shadow-lg backdrop-blur sm:static sm:flex-row sm:items-center sm:justify-between sm:shadow-sm">
          <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-muted-foreground sm:text-sm">
            <span>
              Kategórie:{" "}
              <strong className="text-foreground">
                {selectedCategoryIds.length}
              </strong>
            </span>
            <span>
              Počet otázok:{" "}
              <strong className="text-foreground">{questionCount}</strong>
            </span>
            <span>
              Režim:{" "}
              <strong className="text-foreground">
                {testMode === "training" ? "Trénovací režim" : "Testovací režim"}
              </strong>
            </span>
            {orderMode === "sequential" && (
              <span>
                Rozsah:{" "}
                <strong className="text-primary font-semibold">
                  č. {startQuestionNumber} – {startQuestionNumber + questionCount - 1}
                </strong>
              </span>
            )}
            <span>
              Časovač:{" "}
              <strong className="text-foreground">
                {timeLimitMinutes > 0
                  ? `${timeLimitMinutes} min`
                  : "Bez limitu (Stopky)"}
              </strong>
            </span>
          </div>

          <Button
            type="submit"
            size="lg"
            className="w-full sm:w-auto"
            disabled={isLoading || selectedCategoryIds.length === 0}
          >
            {isLoading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Pripravujem {testMode === "training" ? "tréning" : "test"}...
              </>
            ) : (
              <>
                <Play className="h-4 w-4" />
                {testMode === "training" ? "Spustiť tréning" : "Spustiť test"}
              </>
            )}
          </Button>
        </div>
      </form>
    );
  }

  // ==========================================================================
  // 2. OBRAZOVKA: TESTOVACÍ ENGINE (JEDNA OTÁZKA NARAZ + ČASOVAČ)
  // ==========================================================================
  if (stage === "running") {
    const currentQuestion = activeQuestions[currentIndex];
    const totalQuestions = activeQuestions.length;
    const isFirstQuestion = currentIndex === 0;
    const isLastQuestion = currentIndex === totalQuestions - 1;
    const selectedForCurrent = answersMap[currentQuestion.id] ?? [];
    const meta = categoryMetaMap.get(currentQuestion.category_id);

    const answeredCount = activeQuestions.filter(
      (q) => (answersMap[q.id]?.length ?? 0) > 0
    ).length;

    const isTrainingMode = testMode === "training";

    const evaluatedList = Object.values(evaluatedQuestionsMap);
    const evaluatedCount = evaluatedList.length;
    const evaluatedCorrectCount = evaluatedList.filter((e) => e.isCorrect).length;

    // V testovacom režime (exam) nikdy nezobrazujeme správne odpovede počas testu
    const currentEval = isTrainingMode ? evaluatedQuestionsMap[currentQuestion.id] : undefined;
    const isCurrentEvaluated = Boolean(currentEval);

    const progressPercent = Math.round(
      ((currentIndex + 1) / totalQuestions) * 100
    );

    // Prechod na ďalšiu otázku (v trénovacom režime po označení odpovedí najprv overí a zobrazí vysvetlenie)
    const handleNextQuestion = async () => {
      if (isLoading || isTimerPaused || isEvaluatingSingle) return;

      if (isTrainingMode) {
        const isAlreadyEvaluated = Boolean(evaluatedQuestionsMap[currentQuestion.id]);
        const hasSelectedAnswers = selectedForCurrent.length > 0;

        // V trénovacom režime: po označení odpovedí sa pri prechode na ďalšiu otázku
        // otázka najprv vyhodnotí, aby si študent mohol pozrieť správne odpovede a oficiálne vysvetlenie.
        if (!isAlreadyEvaluated && hasSelectedAnswers) {
          await handleEvaluateSingleQuestion(currentQuestion.id);
          return;
        }
      }

      if (!isLastQuestion) {
        setCurrentIndex((prev) => Math.min(totalQuestions - 1, prev + 1));
      } else if (isTrainingMode) {
        // Na poslednej otázke po vyhodnotení uzavrieme a vyhodnotíme celý tréning
        void submitTestEvaluation(false);
      }
    };

    // Štýlovanie časovača podľa zostávajúceho času
    const isLowTime =
      remainingSeconds !== null &&
      remainingSeconds <= 120 &&
      remainingSeconds > 30;
    const isCriticalTime =
      remainingSeconds !== null && remainingSeconds <= 30;

    let timerBadgeClasses =
      "border-border bg-card text-foreground";
    if (isCriticalTime) {
      timerBadgeClasses =
        "border-red-500 bg-red-500/10 text-red-600 animate-pulse font-bold";
    } else if (isLowTime) {
      timerBadgeClasses =
        "border-amber-500 bg-amber-500/10 text-amber-700 font-semibold";
    }

    return (
      <div className="space-y-4 pb-24 sm:space-y-6 sm:pb-8">
        {errorMessage && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Chyba</AlertTitle>
            <AlertDescription>{errorMessage}</AlertDescription>
          </Alert>
        )}

        {/* Sticky horná lišta s Časovačom a Progresom */}
        <div className="sticky top-14 z-30 -mx-4 border-b bg-background/95 px-4 py-3 backdrop-blur sm:top-16 sm:mx-0 sm:rounded-xl sm:border sm:p-4 sm:shadow-sm">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div className="flex flex-wrap items-center gap-2 sm:gap-3">
              <span className="text-sm font-bold sm:text-base">
                Otázka {currentIndex + 1} / {totalQuestions}
              </span>
              <Badge variant="secondary" className="text-xs">
                Zodpovedané: {answeredCount}/{totalQuestions}
              </Badge>
              {isTrainingMode && evaluatedCount > 0 && (
                <Badge
                  variant="outline"
                  className="hidden xs:inline-flex text-xs border-emerald-500/40 text-emerald-700 bg-emerald-50/50 dark:bg-emerald-950/40 dark:text-emerald-300 font-semibold"
                >
                  Skontrolované: {evaluatedCorrectCount}/{evaluatedCount} správne
                </Badge>
              )}
            </div>

            {/* Časovač + Pauza + Ukončiť */}
            <div className="flex items-center gap-2">
              <div
                className={`inline-flex items-center gap-1.5 rounded-lg border px-2.5 py-1 text-xs font-mono sm:px-3 sm:py-1.5 sm:text-sm ${timerBadgeClasses}`}
              >
                <Clock className="h-3.5 w-3.5 shrink-0 sm:h-4 sm:w-4" />
                <span>
                  {remainingSeconds !== null
                    ? formatSecondsToMMSS(remainingSeconds)
                    : formatSecondsToMMSS(elapsedSeconds)}
                </span>
              </div>

              <Button
                type="button"
                variant="outline"
                size="sm"
                className="h-8 px-2.5 text-xs"
                onClick={() => setIsTimerPaused((prev) => !prev)}
                title={
                  isTimerPaused ? "Pokračovať v teste" : "Pozastaviť časovač"
                }
              >
                {isTimerPaused ? (
                  <>
                    <Play className="h-3.5 w-3.5 text-emerald-600" />
                    <span className="hidden sm:inline">Pokračovať</span>
                  </>
                ) : (
                  <>
                    <Pause className="h-3.5 w-3.5" />
                    <span className="hidden sm:inline">Pauza</span>
                  </>
                )}
              </Button>

              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="h-8 px-2 text-xs text-muted-foreground hover:text-foreground"
                onClick={() => void submitTestEvaluation(false)}
                disabled={isLoading}
                title="Predčasne ukončiť test a vyhodnotiť"
              >
                Ukončiť test
              </Button>
            </div>
          </div>

          {/* Progres bar */}
          <div className="mt-2.5 h-1.5 w-full overflow-hidden rounded-full bg-secondary sm:h-2">
            <div
              className="h-full bg-primary transition-all duration-300"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
        </div>

        {/* Info baner pri pozastavenom časovači */}
        {isTimerPaused && (
          <Alert>
            <Pause className="h-4 w-4" />
            <AlertTitle>Test je pozastavený</AlertTitle>
            <AlertDescription className="flex flex-wrap items-center justify-between gap-2">
              <span>
                Časovač je momentálne zastavený. Kliknite na Pokračovať pre
                návrat k odpovedaniu.
              </span>
              <Button
                type="button"
                size="sm"
                onClick={() => setIsTimerPaused(false)}
              >
                Pokračovať v teste
              </Button>
            </AlertDescription>
          </Alert>
        )}

        {/* Karta aktuálnej otázky */}
        <Card
          className={`shadow-sm transition-opacity ${
            isTimerPaused ? "pointer-events-none opacity-50" : ""
          }`}
        >
          <CardHeader className="space-y-2.5 p-4 sm:space-y-3 sm:p-6">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div className="flex flex-wrap items-center gap-2">
                {meta && (
                  <Badge variant="outline" className="max-w-full truncate text-xs">
                    {meta.subjectName} • {meta.categoryName}
                  </Badge>
                )}
                {currentQuestion.questionNumber && (
                  <Badge
                    variant="secondary"
                    className="border border-primary/25 bg-primary/10 text-xs font-semibold text-primary"
                  >
                    Otázka číslo {currentQuestion.questionNumber}
                  </Badge>
                )}
              </div>

              <div className="flex items-center gap-2">
                {isCurrentEvaluated && (
                  <Badge
                    className={
                      currentEval?.isCorrect
                        ? "bg-emerald-600 text-white text-xs gap-1 hover:bg-emerald-600"
                        : "bg-red-600 text-white text-xs gap-1 hover:bg-red-600"
                    }
                  >
                    {currentEval?.isCorrect ? (
                      <>
                        <CheckCircle2 className="h-3 w-3" />
                        Správne (+1)
                      </>
                    ) : (
                      <>
                        <XCircle className="h-3 w-3" />
                        Nesprávne (0)
                      </>
                    )}
                  </Badge>
                )}
                <Badge
                  variant={
                    currentQuestion.isMultipleChoice ? "default" : "secondary"
                  }
                  className="text-xs"
                >
                  {currentQuestion.isMultipleChoice
                    ? "Viac správnych (Checkbox)"
                    : "1 správna (Rádio)"}
                </Badge>
              </div>
            </div>

            <CardTitle className="text-base leading-relaxed sm:text-xl">
              {currentQuestion.content}
            </CardTitle>
          </CardHeader>

          <CardContent className="space-y-3 p-4 pt-0 sm:space-y-3 sm:p-6 sm:pt-0">
            {currentQuestion.options.map((option) => {
              const isChecked = selectedForCurrent.includes(option.id);
              const isCorrectAnswer =
                currentEval?.correctAnswers.includes(option.id) ?? false;

              let optionContainerClass =
                "border-border bg-background hover:bg-accent/50";
              let badgeIdClass = "border bg-muted/50 text-muted-foreground";

              if (isCurrentEvaluated) {
                if (isCorrectAnswer) {
                  if (isChecked) {
                    optionContainerClass =
                      "border-emerald-500 bg-emerald-50/80 text-emerald-950 font-medium ring-1 ring-emerald-500 dark:bg-emerald-950/40 dark:text-emerald-200";
                    badgeIdClass =
                      "bg-emerald-600 text-white border-emerald-600";
                  } else {
                    optionContainerClass =
                      "border-emerald-500/80 border-dashed bg-emerald-50/30 text-emerald-950 dark:bg-emerald-950/20 dark:text-emerald-300";
                    badgeIdClass =
                      "border-emerald-500 bg-emerald-100 text-emerald-800 dark:bg-emerald-900/60 dark:text-emerald-300";
                  }
                } else {
                  if (isChecked) {
                    optionContainerClass =
                      "border-destructive bg-destructive/10 text-destructive font-medium ring-1 ring-destructive";
                    badgeIdClass =
                      "bg-destructive text-white border-destructive";
                  } else {
                    optionContainerClass =
                      "border-border/60 bg-muted/10 opacity-70";
                    badgeIdClass = "border bg-muted/30 text-muted-foreground";
                  }
                }
              } else if (isChecked) {
                optionContainerClass =
                  "border-primary bg-primary/5 font-medium ring-1 ring-primary";
                badgeIdClass =
                  "bg-primary text-primary-foreground border-primary";
              }

              return (
                <label
                  key={option.id}
                  className={`flex min-h-[52px] touch-manipulation items-center justify-between gap-3 rounded-xl border p-3.5 text-sm transition-all sm:gap-3.5 sm:p-4 ${
                    isCurrentEvaluated
                      ? "cursor-default"
                      : "cursor-pointer active:scale-[0.99]"
                  } ${optionContainerClass}`}
                >
                  <div className="flex items-center gap-3 sm:gap-3.5">
                    <input
                      type={
                        currentQuestion.isMultipleChoice ? "checkbox" : "radio"
                      }
                      name={`question-${currentQuestion.id}`}
                      value={option.id}
                      checked={isChecked}
                      disabled={isCurrentEvaluated || isTimerPaused}
                      onChange={() =>
                        handleOptionChange(
                          currentQuestion.id,
                          option.id,
                          currentQuestion.isMultipleChoice
                        )
                      }
                      className="h-4 w-4 shrink-0 border-input text-primary focus:ring-primary sm:h-5 sm:w-5 disabled:opacity-70"
                    />
                    <span
                      className={`flex h-6 w-6 shrink-0 items-center justify-center rounded text-xs font-semibold uppercase sm:h-7 sm:w-7 ${badgeIdClass}`}
                    >
                      {option.id}
                    </span>
                    <span className="text-sm leading-snug sm:text-base">
                      {option.text}
                    </span>
                  </div>

                  {/* Vizuálny odznak po vyhodnotení */}
                  {isCurrentEvaluated && (
                    <div className="shrink-0 flex items-center gap-1.5 text-xs font-semibold">
                      {isCorrectAnswer && isChecked && (
                        <span className="flex items-center gap-1 text-emerald-600 dark:text-emerald-400">
                          <CheckCircle2 className="h-4 w-4 shrink-0" />
                          <span className="hidden sm:inline">Správne označené</span>
                        </span>
                      )}
                      {isCorrectAnswer && !isChecked && (
                        <span className="text-[11px] rounded bg-emerald-100 dark:bg-emerald-950 px-2 py-0.5 text-emerald-800 dark:text-emerald-300 border border-emerald-500/40">
                          Mala byť označená
                        </span>
                      )}
                      {!isCorrectAnswer && isChecked && (
                        <span className="flex items-center gap-1 text-destructive">
                          <XCircle className="h-4 w-4 shrink-0" />
                          <span className="hidden sm:inline">Nesprávne</span>
                        </span>
                      )}
                    </div>
                  )}
                </label>
              );
            })}

            {/* Informačný blok po okamžitom vyhodnotení */}
            {isCurrentEvaluated && currentEval && (
              <div
                className={`rounded-xl border p-4 text-sm space-y-2.5 animate-in fade-in duration-200 ${
                  currentEval.isCorrect
                    ? "border-emerald-500/40 bg-emerald-50/70 text-emerald-950 dark:bg-emerald-950/30 dark:text-emerald-200"
                    : "border-red-500/40 bg-red-50/70 text-red-950 dark:bg-red-950/30 dark:text-red-200"
                }`}
              >
                <div className="flex flex-wrap items-center justify-between gap-2 font-bold text-sm sm:text-base">
                  <div className="flex items-center gap-2">
                    {currentEval.isCorrect ? (
                      <>
                        <CheckCircle2 className="h-5 w-5 text-emerald-600 dark:text-emerald-400 shrink-0" />
                        <span>Správna odpoveď! (+1 bod)</span>
                      </>
                    ) : (
                      <>
                        <XCircle className="h-5 w-5 text-red-600 dark:text-red-400 shrink-0" />
                        <span>Nesprávna odpoveď (0 bodov)</span>
                      </>
                    )}
                  </div>
                  <Badge
                    variant="outline"
                    className={
                      currentEval.isCorrect
                        ? "border-emerald-500 text-emerald-700 bg-background font-semibold"
                        : "border-red-500 text-red-700 bg-background font-semibold"
                    }
                  >
                    Správne: {currentEval.correctAnswers.map((a) => a.toUpperCase()).join(", ")}
                  </Badge>
                </div>

                {currentEval.explanation && (
                  <div className="pt-2 text-xs sm:text-sm text-foreground/85 border-t border-border/40">
                    <p className="font-semibold text-foreground">Oficiálne vysvetlenie UPJŠ LF:</p>
                    <p className="mt-0.5 leading-relaxed">{currentEval.explanation}</p>
                  </div>
                )}
              </div>
            )}
          </CardContent>

          {/* Desktop/Tablet pätička s tlačidlami */}
          <CardFooter className="hidden items-center justify-between gap-3 border-t p-6 pt-4 sm:flex">
            <Button
              type="button"
              variant="outline"
              onClick={() => setCurrentIndex((prev) => Math.max(0, prev - 1))}
              disabled={isFirstQuestion || isLoading || isEvaluatingSingle}
            >
              <ArrowLeft className="h-4 w-4" />
              Predchádzajúca
            </Button>

            <div className="flex items-center gap-3">
              {/* Tlačidlo Skontrolovať otázku (len v trénovacom režime a ak ešte nebola vyhodnotená) */}
              {isTrainingMode && !isCurrentEvaluated && (
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => handleEvaluateSingleQuestion(currentQuestion.id)}
                  disabled={
                    isEvaluatingSingle ||
                    isLoading ||
                    isTimerPaused ||
                    selectedForCurrent.length === 0
                  }
                  className="gap-1.5 border-amber-500/40 text-amber-600 hover:bg-amber-50 hover:text-amber-700 dark:border-amber-500/30 dark:text-amber-400 dark:hover:bg-amber-950/30"
                >
                  {isEvaluatingSingle ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      Overujem odpoveď...
                    </>
                  ) : (
                    <>
                      <Zap className="h-4 w-4" />
                      Skontrolovať otázku
                    </>
                  )}
                </Button>
              )}

              {!isLastQuestion ? (
                <Button
                  type="button"
                  onClick={handleNextQuestion}
                  disabled={isLoading || isEvaluatingSingle}
                  className={
                    isTrainingMode && !isCurrentEvaluated && selectedForCurrent.length > 0
                      ? "bg-amber-600 hover:bg-amber-700 text-white font-semibold shadow-sm"
                      : ""
                  }
                >
                  {isEvaluatingSingle ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      Vyhodnocujem...
                    </>
                  ) : isTrainingMode && !isCurrentEvaluated && selectedForCurrent.length > 0 ? (
                    <>
                      <Zap className="h-4 w-4" />
                      Vyhodnotiť a pokračovať
                      <ArrowRight className="h-4 w-4" />
                    </>
                  ) : (
                    <>
                      Ďalšia otázka
                      <ArrowRight className="h-4 w-4" />
                    </>
                  )}
                </Button>
              ) : (
                <Button
                  type="button"
                  onClick={
                    isTrainingMode && !isCurrentEvaluated && selectedForCurrent.length > 0
                      ? handleNextQuestion
                      : () => void submitTestEvaluation(false)
                  }
                  disabled={isLoading || isEvaluatingSingle}
                  className="bg-emerald-600 text-white hover:bg-emerald-700 font-semibold"
                >
                  {isLoading || isEvaluatingSingle ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      Vyhodnocujem...
                    </>
                  ) : isTrainingMode && !isCurrentEvaluated && selectedForCurrent.length > 0 ? (
                    <>
                      <Zap className="h-4 w-4" />
                      Vyhodnotiť poslednú otázku
                    </>
                  ) : (
                    <>
                      <ClipboardCheck className="h-4 w-4" />
                      {isTrainingMode
                        ? "Ukončiť tréning a zobraziť výsledky"
                        : `Vyhodnotiť test (${totalQuestions} otázok)`}
                    </>
                  )}
                </Button>
              )}
            </div>
          </CardFooter>
        </Card>

        {/* Rýchla navigácia medzi číslami otázok (horizontálny scroll na mobile, mriežka na tablete/desktope) */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between text-xs text-muted-foreground">
            <span className="font-medium">
              Prehľad otázok testu ({totalQuestions} otázok):
            </span>
            <div className="flex items-center gap-3 text-[11px]">
              {isTrainingMode && (
                <>
                  <span className="flex items-center gap-1">
                    <span className="h-2 w-2 rounded-full bg-emerald-500" /> Správne
                  </span>
                  <span className="flex items-center gap-1">
                    <span className="h-2 w-2 rounded-full bg-red-500" /> Nesprávne
                  </span>
                </>
              )}
              <span className="flex items-center gap-1">
                <span className="h-2 w-2 rounded-full bg-primary" /> Označené
              </span>
            </div>
          </div>
          <div className="flex items-center gap-1.5 overflow-x-auto pb-2 sm:flex-wrap sm:max-h-52 sm:overflow-y-auto sm:p-2 sm:rounded-xl sm:border sm:bg-muted/15">
            {activeQuestions.map((q, idx) => {
              const hasAnswer = (answersMap[q.id]?.length ?? 0) > 0;
              const isCurrent = idx === currentIndex;
              const evalRes = isTrainingMode ? evaluatedQuestionsMap[q.id] : undefined;

              let btnClass =
                "border-border bg-card text-muted-foreground hover:bg-accent";
              if (evalRes) {
                btnClass = evalRes.isCorrect
                  ? "border-emerald-600 bg-emerald-600 text-white font-bold shadow-sm"
                  : "border-red-600 bg-red-600 text-white font-bold shadow-sm";
              } else if (hasAnswer) {
                btnClass =
                  "border-primary/40 bg-primary/10 text-primary font-semibold";
              }

              return (
                <button
                  key={q.id}
                  type="button"
                  onClick={() => setCurrentIndex(idx)}
                  title={`Otázka ${idx + 1}${
                    q.questionNumber ? ` (č. ${q.questionNumber})` : ""
                  }${
                    evalRes
                      ? evalRes.isCorrect
                        ? " - Správne"
                        : " - Nesprávne"
                      : hasAnswer
                      ? " - Označená"
                      : ""
                  }`}
                  className={`flex h-8.5 min-w-8.5 px-1.5 shrink-0 touch-manipulation items-center justify-center rounded-lg border text-xs font-semibold transition-all ${
                    isCurrent
                      ? "ring-2 ring-primary ring-offset-2 ring-offset-background"
                      : ""
                  } ${btnClass}`}
                >
                  {q.questionNumber ?? idx + 1}
                </button>
              );
            })}
          </div>
        </div>

        {/* Spodná fixná lišta pre pohodlné ovládanie palcom na mobile */}
        <div className="fixed inset-x-0 bottom-0 z-40 flex items-center justify-between gap-2 border-t bg-card/95 p-3 shadow-lg backdrop-blur sm:hidden">
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => setCurrentIndex((prev) => Math.max(0, prev - 1))}
            disabled={isFirstQuestion || isLoading || isEvaluatingSingle}
          >
            <ArrowLeft className="h-4 w-4" />
          </Button>

          {isTrainingMode && !isCurrentEvaluated && selectedForCurrent.length > 0 && (
            <Button
              type="button"
              variant="outline"
              size="default"
              className="border-amber-500/40 text-amber-600 hover:bg-amber-50 hover:text-amber-700 dark:border-amber-500/30 dark:text-amber-400 dark:hover:bg-amber-950/30"
              onClick={() => handleEvaluateSingleQuestion(currentQuestion.id)}
              disabled={
                isEvaluatingSingle ||
                isLoading ||
                isTimerPaused
              }
            >
              {isEvaluatingSingle ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <>
                  <Zap className="h-4 w-4" />
                  Overiť
                </>
              )}
            </Button>
          )}

          {!isLastQuestion ? (
            <Button
              type="button"
              size="default"
              className={`flex-1 ${
                isTrainingMode && !isCurrentEvaluated && selectedForCurrent.length > 0
                  ? "bg-amber-600 hover:bg-amber-700 text-white font-semibold"
                  : ""
              }`}
              onClick={handleNextQuestion}
              disabled={isLoading || isEvaluatingSingle}
            >
              {isEvaluatingSingle ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Overujem...
                </>
              ) : isTrainingMode && !isCurrentEvaluated && selectedForCurrent.length > 0 ? (
                <>
                  <Zap className="h-4 w-4" />
                  Vyhodnotiť a ďalej
                  <ArrowRight className="h-4 w-4" />
                </>
              ) : (
                <>
                  Ďalšia
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </Button>
          ) : (
            <Button
              type="button"
              size="default"
              onClick={
                isTrainingMode && !isCurrentEvaluated && selectedForCurrent.length > 0
                  ? handleNextQuestion
                  : () => void submitTestEvaluation(false)
              }
              disabled={isLoading || isEvaluatingSingle}
              className="flex-1 bg-emerald-600 text-white hover:bg-emerald-700 font-semibold"
            >
              {isLoading || isEvaluatingSingle ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Ukladám...
                </>
              ) : isTrainingMode && !isCurrentEvaluated && selectedForCurrent.length > 0 ? (
                <>
                  <Zap className="h-4 w-4" />
                  Vyhodnotiť
                </>
              ) : (
                <>
                  <ClipboardCheck className="h-4 w-4" />
                  {isTrainingMode ? "Dokončiť tréning" : "Vyhodnotiť test"}
                </>
              )}
            </Button>
          )}
        </div>
      </div>
    );
  }

  // ==========================================================================
  // 3. OBRAZOVKA: VYHODNOTENIE TESTU (RESULTS + ŠTATISTIKA ČASU)
  // ==========================================================================
  if (stage === "results" && evaluation) {
    const { totalQuestions, correctCount, scorePercentage, results } =
      evaluation;
    const incorrectCount = totalQuestions - correctCount;
    const avgSecondsPerQuestion =
      totalQuestions > 0 ? Math.round(elapsedSeconds / totalQuestions) : 0;

    return (
      <div className="space-y-6 pb-8 sm:space-y-8">
        {timedOut && (
          <Alert variant="destructive">
            <Clock className="h-4 w-4" />
            <AlertTitle>Časový limit vypršal!</AlertTitle>
            <AlertDescription>
              Váš čas na vypracovanie testu uplynul, preto bol test automaticky
              ukončený a vyhodnotený.
            </AlertDescription>
          </Alert>
        )}

        {/* Súhrnná karta výsledku */}
        <Card className="border-primary/20 shadow-sm">
          <CardHeader className="p-5 text-center sm:p-6">
            <div className="mx-auto mb-2 flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary sm:h-14 sm:w-14">
              <Trophy className="h-6 w-6 sm:h-7 sm:w-7" />
            </div>
            <CardTitle className="text-2xl font-bold sm:text-3xl">
              Úspešnosť testu: {scorePercentage} %
            </CardTitle>
            <CardDescription className="text-xs sm:text-base">
              Všetky odpovede boli uložené do vašej histórie v{" "}
              <code>user_progress</code>.
            </CardDescription>
          </CardHeader>

          <CardContent className="p-4 pt-0 sm:p-6 sm:pt-0">
            <div className="mx-auto grid max-w-2xl grid-cols-2 gap-3 text-center sm:grid-cols-4 sm:gap-4">
              <div className="rounded-xl border bg-muted/30 p-3 sm:p-4">
                <div className="text-xl font-bold sm:text-2xl">
                  {totalQuestions}
                </div>
                <div className="text-xs text-muted-foreground">
                  Celkovo otázok
                </div>
              </div>
              <div className="rounded-xl border border-emerald-500/30 bg-emerald-50/70 p-3 text-emerald-900 sm:p-4">
                <div className="text-xl font-bold sm:text-2xl">
                  {correctCount}
                </div>
                <div className="text-xs">Správne</div>
              </div>
              <div className="rounded-xl border border-red-500/30 bg-red-50/70 p-3 text-red-900 sm:p-4">
                <div className="text-xl font-bold sm:text-2xl">
                  {incorrectCount}
                </div>
                <div className="text-xs">Nesprávne</div>
              </div>
              <div className="rounded-xl border bg-primary/5 p-3 sm:p-4">
                <div className="text-xl font-bold text-primary sm:text-2xl">
                  {formatSecondsToMMSS(elapsedSeconds)}
                </div>
                <div className="text-xs text-muted-foreground">
                  Čas ({avgSecondsPerQuestion}s / otázka)
                </div>
              </div>
            </div>
          </CardContent>

          <CardFooter className="flex justify-center border-t p-4 sm:p-6 sm:pt-4">
            <Button
              onClick={handleResetToBuilder}
              size="lg"
              className="w-full sm:w-auto"
            >
              <RotateCcw className="h-4 w-4" />
              Vytvoriť nový test
            </Button>
          </CardFooter>
        </Card>

        {/* Prehľad všetkých otázok z testu s farebným označením (zelená/červená) a explanation */}
        <div className="space-y-4">
          <h2 className="text-lg font-bold tracking-tight sm:text-xl">
            Podrobný prehľad otázok a vysvetlení
          </h2>

          {results.map((item, idx) => {
            const selectedSet = new Set(item.selectedOptionIds);
            const correctSet = new Set(item.correctAnswers);

            return (
              <Card
                key={item.questionId}
                className={
                  item.isCorrect
                    ? "border-2 border-emerald-500/60 bg-emerald-50/20"
                    : "border-2 border-red-500/60 bg-red-50/20"
                }
              >
                <CardHeader className="p-4 pb-3 sm:p-6 sm:pb-3">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <span className="text-xs font-semibold text-muted-foreground sm:text-sm">
                      Otázka #{idx + 1}
                    </span>
                    {item.isCorrect ? (
                      <Badge className="gap-1 bg-emerald-600 text-xs text-white hover:bg-emerald-600">
                        <CheckCircle2 className="h-3.5 w-3.5" />
                        Správne zodpovedané
                      </Badge>
                    ) : (
                      <Badge variant="destructive" className="gap-1 text-xs">
                        <XCircle className="h-3.5 w-3.5" />
                        Nesprávne zodpovedané
                      </Badge>
                    )}
                  </div>
                  <CardTitle className="pt-1 text-base leading-snug sm:text-lg">
                    {item.content}
                  </CardTitle>
                </CardHeader>

                <CardContent className="space-y-4 p-4 pt-0 sm:p-6 sm:pt-0">
                  {/* Zoznam možností s farebným vyznačením */}
                  <div className="grid gap-2">
                    {item.options.map((opt) => {
                      const wasSelected = selectedSet.has(opt.id);
                      const isCorrectOption = correctSet.has(opt.id);

                      let rowClass = "border-border bg-background";
                      if (isCorrectOption) {
                        rowClass =
                          "border-emerald-500 bg-emerald-100/80 text-emerald-950 font-medium";
                      } else if (wasSelected && !isCorrectOption) {
                        rowClass =
                          "border-red-500 bg-red-100/80 text-red-950 font-medium";
                      }

                      return (
                        <div
                          key={opt.id}
                          className={`flex flex-col justify-between gap-2 rounded-lg border p-3 text-sm sm:flex-row sm:items-center sm:gap-3 ${rowClass}`}
                        >
                          <div className="flex items-start gap-2.5 sm:items-center sm:gap-3">
                            <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded border bg-white/80 text-xs font-semibold uppercase">
                              {opt.id}
                            </span>
                            <span className="leading-snug">{opt.text}</span>
                          </div>

                          <div className="flex shrink-0 items-center justify-end gap-2 text-xs">
                            {wasSelected && (
                              <Badge
                                variant="outline"
                                className="bg-background/90"
                              >
                                Vaša voľba
                              </Badge>
                            )}
                            {isCorrectOption && (
                              <CheckCircle2 className="h-4 w-4 text-emerald-600" />
                            )}
                            {wasSelected && !isCorrectOption && (
                              <XCircle className="h-4 w-4 text-red-600" />
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>

                  {/* Vysvetlenie z databázy (explanation) */}
                  <div className="rounded-lg border bg-card p-3.5 text-sm sm:p-4">
                    <div className="mb-1 flex items-center gap-1.5 font-semibold text-foreground">
                      <Sparkles className="h-4 w-4 text-primary" />
                      Vysvetlenie:
                    </div>
                    <p className="text-xs leading-relaxed text-muted-foreground sm:text-sm">
                      {item.explanation
                        ? item.explanation
                        : "Pre túto otázku nie je v databáze uvedené podrobné vysvetlenie."}
                    </p>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    );
  }

  return null;
}
