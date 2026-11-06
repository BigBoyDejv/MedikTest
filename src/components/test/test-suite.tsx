"use client";

import * as React from "react";
import {
  evaluateTestAction,
  generateTestQuestionsAction,
  type ActiveTestQuestion,
  type QuestionFilterMode,
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
  Filter,
  HelpCircle,
  Layers,
  Loader2,
  Play,
  RotateCcw,
  Sparkles,
  Trophy,
  XCircle,
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

const QUESTION_COUNT_OPTIONS = [10, 20, 50] as const;

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
  const [filterMode, setFilterMode] = React.useState<QuestionFilterMode>(
    initialFilterMode ?? "all"
  );

  // ==========================================================================
  // STAV TESTOVACIEHO ENGINU A VYHODNOTENIA
  // ==========================================================================
  const [stage, setStage] = React.useState<"builder" | "running" | "results">(
    "builder"
  );
  const [activeQuestions, setActiveQuestions] = React.useState<
    ActiveTestQuestion[]
  >([]);
  const [currentIndex, setCurrentIndex] = React.useState<number>(0);
  // Mapa questionId -> pole zvolených option.id
  const [answersMap, setAnswersMap] = React.useState<Record<string, string[]>>(
    {}
  );
  const [evaluation, setEvaluation] =
    React.useState<TestEvaluationSummary | null>(null);

  const [isLoading, setIsLoading] = React.useState(false);
  const [errorMessage, setErrorMessage] = React.useState<string | null>(null);

  // Mapa pre rýchle zobrazenie názvu kategórie a predmetu pri otázke
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
      });

      if (response.error || !response.questions) {
        setErrorMessage(
          response.error ?? "Nepodarilo sa načítať otázky pre test."
        );
        return;
      }

      setActiveQuestions(response.questions);
      setAnswersMap({});
      setCurrentIndex(0);
      setEvaluation(null);
      setStage("running");
    } finally {
      setIsLoading(false);
    }
  }

  // Výber odpovede počas testu (Checkbox pre Multiple Choice, Rádio pre Single Choice)
  function handleOptionChange(
    questionId: string,
    optionId: string,
    isMultipleChoice: boolean
  ) {
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

  // Odoslanie celého testu na vyhodnotenie a uloženie do user_progress
  async function handleEvaluateTest() {
    setErrorMessage(null);
    setIsLoading(true);

    try {
      const submissions = activeQuestions.map((q) => ({
        questionId: q.id,
        selectedOptionIds: answersMap[q.id] ?? [],
      }));

      const response = await evaluateTestAction(submissions);

      if (response.error || !response.evaluation) {
        setErrorMessage(
          response.error ?? "Nepodarilo sa vyhodnotiť test."
        );
        return;
      }

      setEvaluation(response.evaluation);
      setStage("results");
      window.scrollTo({ top: 0, behavior: "smooth" });
    } finally {
      setIsLoading(false);
    }
  }

  function handleResetToBuilder() {
    setStage("builder");
    setActiveQuestions([]);
    setAnswersMap({});
    setCurrentIndex(0);
    setEvaluation(null);
    setErrorMessage(null);
  }

  // ==========================================================================
  // 1. OBRAZOVKA: KONFIGURÁTOR TESTU (TEST BUILDER)
  // ==========================================================================
  if (stage === "builder") {
    return (
      <form onSubmit={handleStartTest} className="space-y-6">
        {errorMessage && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Upozornenie</AlertTitle>
            <AlertDescription>{errorMessage}</AlertDescription>
          </Alert>
        )}

        {/* Krok 1: Výber kategórií */}
        <Card>
          <CardHeader>
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div>
                <CardTitle className="flex items-center gap-2 text-lg">
                  <Layers className="h-5 w-5 text-primary" />
                  1. Vyberte kategórie otázok
                </CardTitle>
                <CardDescription className="mt-1">
                  Zaškrtnite tematické okruhy, z ktorých chcete zostaviť test.
                </CardDescription>
              </div>

              <div className="flex items-center gap-2">
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => setSelectedCategoryIds(allCategoryIds)}
                >
                  <CheckCheck className="h-4 w-4" />
                  Vybrať všetky
                </Button>
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  onClick={() => setSelectedCategoryIds([])}
                >
                  Zrušiť výber
                </Button>
              </div>
            </div>
          </CardHeader>

          <CardContent className="space-y-6">
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
                    className="space-y-3 rounded-xl border bg-muted/20 p-4"
                  >
                    <div className="flex items-center justify-between border-b pb-2.5">
                      <div className="flex items-center gap-2 font-semibold">
                        <BookOpen className="h-4 w-4 text-primary" />
                        <span>{subject.name}</span>
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

                    <div className="grid gap-2.5 sm:grid-cols-2 md:grid-cols-3">
                      {subject.categories.map((cat) => {
                        const isChecked = selectedCategoryIds.includes(cat.id);
                        return (
                          <label
                            key={cat.id}
                            className={`flex cursor-pointer items-center justify-between gap-3 rounded-lg border p-3 text-sm transition-colors ${
                              isChecked
                                ? "border-primary bg-primary/5 font-medium"
                                : "border-border bg-background hover:bg-accent/50"
                            }`}
                          >
                            <div className="flex items-center gap-2.5">
                              <input
                                type="checkbox"
                                checked={isChecked}
                                onChange={() => toggleCategory(cat.id)}
                                className="h-4 w-4 rounded border-input text-primary focus:ring-primary"
                              />
                              <span>{cat.name}</span>
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

        {/* Krok 2 a 3: Počet otázok a Filter */}
        <div className="grid gap-6 md:grid-cols-2">
          {/* Krok 2: Počet otázok */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <HelpCircle className="h-5 w-5 text-primary" />
                2. Počet otázok v teste
              </CardTitle>
              <CardDescription>
                Zvoľte koľko otázok sa má vygenerovať do testu.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-3 gap-3">
                {QUESTION_COUNT_OPTIONS.map((count) => {
                  const isSelected = questionCount === count;
                  return (
                    <button
                      key={count}
                      type="button"
                      onClick={() => setQuestionCount(count)}
                      className={`flex flex-col items-center justify-center rounded-xl border p-4 transition-all ${
                        isSelected
                          ? "border-primary bg-primary text-primary-foreground shadow-sm"
                          : "border-border bg-background hover:bg-accent"
                      }`}
                    >
                      <span className="text-2xl font-bold">{count}</span>
                      <span
                        className={`text-xs ${
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
            </CardContent>
          </Card>

          {/* Krok 3: Filter otázok podľa user_progress */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <Filter className="h-5 w-5 text-primary" />
                3. Filter otázok
              </CardTitle>
              <CardDescription>
                Filtrovanie otázok na základe vašej histórie odpovedí (
                <code>user_progress</code>).
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-2.5">
              {FILTER_OPTIONS.map((option) => {
                const isSelected = filterMode === option.value;
                return (
                  <label
                    key={option.value}
                    className={`flex cursor-pointer items-start gap-3 rounded-lg border p-3 text-sm transition-colors ${
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
                      className="mt-0.5 h-4 w-4 border-input text-primary focus:ring-primary"
                    />
                    <div className="space-y-0.5">
                      <div className="font-medium text-foreground">
                        {option.label}
                      </div>
                      <p className="text-xs text-muted-foreground">
                        {option.description}
                      </p>
                    </div>
                  </label>
                );
              })}
            </CardContent>
          </Card>
        </div>

        {/* Tlačidlo na spustenie testu */}
        <div className="flex items-center justify-between rounded-xl border bg-card p-4 shadow-sm">
          <div className="text-sm text-muted-foreground">
            Zvolených kategórií:{" "}
            <strong className="text-foreground">
              {selectedCategoryIds.length}
            </strong>{" "}
            | Max. počet otázok:{" "}
            <strong className="text-foreground">{questionCount}</strong>
          </div>

          <Button
            type="submit"
            size="lg"
            disabled={isLoading || selectedCategoryIds.length === 0}
          >
            {isLoading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Pripravujem test...
              </>
            ) : (
              <>
                <Play className="h-4 w-4" />
                Spustiť test
              </>
            )}
          </Button>
        </div>
      </form>
    );
  }

  // ==========================================================================
  // 2. OBRAZOVKA: TESTOVACÍ ENGINE (JEDNA OTÁZKA NARAZ)
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

    const progressPercent = Math.round(
      ((currentIndex + 1) / totalQuestions) * 100
    );

    return (
      <div className="space-y-6">
        {errorMessage && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Chyba</AlertTitle>
            <AlertDescription>{errorMessage}</AlertDescription>
          </Alert>
        )}

        {/* Horný progres bar a prehľad otázok */}
        <div className="space-y-2">
          <div className="flex flex-wrap items-center justify-between gap-2 text-sm">
            <span className="font-semibold">
              Otázka {currentIndex + 1} z {totalQuestions}
            </span>
            <span className="text-muted-foreground">
              Zodpovedané: {answeredCount} / {totalQuestions}
            </span>
          </div>
          <div className="h-2 w-full overflow-hidden rounded-full bg-secondary">
            <div
              className="h-full bg-primary transition-all duration-300"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
        </div>

        {/* Karta aktuálnej otázky */}
        <Card className="shadow-sm">
          <CardHeader className="space-y-3">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div className="flex flex-wrap items-center gap-2">
                {meta && (
                  <Badge variant="outline">
                    {meta.subjectName} • {meta.categoryName}
                  </Badge>
                )}
              </div>

              <Badge
                variant={
                  currentQuestion.isMultipleChoice ? "default" : "secondary"
                }
              >
                {currentQuestion.isMultipleChoice
                  ? "Viac správnych odpovedí (Checkbox)"
                  : "Jedna správna odpoveď (Rádio)"}
              </Badge>
            </div>

            <CardTitle className="text-xl leading-relaxed">
              {currentQuestion.content}
            </CardTitle>
          </CardHeader>

          <CardContent className="space-y-3">
            {currentQuestion.options.map((option) => {
              const isChecked = selectedForCurrent.includes(option.id);
              return (
                <label
                  key={option.id}
                  className={`flex cursor-pointer items-center gap-3.5 rounded-xl border p-4 text-sm transition-all ${
                    isChecked
                      ? "border-primary bg-primary/5 ring-1 ring-primary font-medium"
                      : "border-border bg-background hover:bg-accent/50"
                  }`}
                >
                  <input
                    type={
                      currentQuestion.isMultipleChoice ? "checkbox" : "radio"
                    }
                    name={`question-${currentQuestion.id}`}
                    value={option.id}
                    checked={isChecked}
                    onChange={() =>
                      handleOptionChange(
                        currentQuestion.id,
                        option.id,
                        currentQuestion.isMultipleChoice
                      )
                    }
                    className="h-4 w-4 shrink-0 border-input text-primary focus:ring-primary"
                  />
                  <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded border bg-muted/50 text-xs font-semibold uppercase">
                    {option.id}
                  </span>
                  <span className="text-base">{option.text}</span>
                </label>
              );
            })}
          </CardContent>

          <CardFooter className="flex flex-wrap items-center justify-between gap-3 border-t pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => setCurrentIndex((prev) => Math.max(0, prev - 1))}
              disabled={isFirstQuestion || isLoading}
            >
              <ArrowLeft className="h-4 w-4" />
              Predchádzajúca
            </Button>

            <div className="flex items-center gap-3">
              {!isLastQuestion ? (
                <Button
                  type="button"
                  onClick={() =>
                    setCurrentIndex((prev) =>
                      Math.min(totalQuestions - 1, prev + 1)
                    )
                  }
                >
                  Ďalšia
                  <ArrowRight className="h-4 w-4" />
                </Button>
              ) : (
                <Button
                  type="button"
                  onClick={handleEvaluateTest}
                  disabled={isLoading}
                  className="bg-emerald-600 text-white hover:bg-emerald-700"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      Vyhodnocujem a ukladám...
                    </>
                  ) : (
                    <>
                      <ClipboardCheck className="h-4 w-4" />
                      Vyhodnotiť test
                    </>
                  )}
                </Button>
              )}
            </div>
          </CardFooter>
        </Card>

        {/* Rýchla navigácia medzi číslami otázok */}
        <div className="flex flex-wrap items-center gap-2">
          {activeQuestions.map((q, idx) => {
            const hasAnswer = (answersMap[q.id]?.length ?? 0) > 0;
            const isCurrent = idx === currentIndex;
            return (
              <button
                key={q.id}
                type="button"
                onClick={() => setCurrentIndex(idx)}
                className={`flex h-9 w-9 items-center justify-center rounded-lg border text-xs font-semibold transition-all ${
                  isCurrent
                    ? "border-primary bg-primary text-primary-foreground"
                    : hasAnswer
                      ? "border-primary/40 bg-primary/10 text-primary"
                      : "border-border bg-card text-muted-foreground hover:bg-accent"
                }`}
              >
                {idx + 1}
              </button>
            );
          })}
        </div>
      </div>
    );
  }

  // ==========================================================================
  // 3. OBRAZOVKA: VYHODNOTENIE TESTU (RESULTS)
  // ==========================================================================
  if (stage === "results" && evaluation) {
    const { totalQuestions, correctCount, scorePercentage, results } =
      evaluation;
    const incorrectCount = totalQuestions - correctCount;

    return (
      <div className="space-y-8">
        {/* Súhrnná karta výsledku */}
        <Card className="border-primary/20 shadow-sm">
          <CardHeader className="text-center">
            <div className="mx-auto mb-2 flex h-14 w-14 items-center justify-center rounded-full bg-primary/10 text-primary">
              <Trophy className="h-7 w-7" />
            </div>
            <CardTitle className="text-3xl font-bold">
              Úspešnosť testu: {scorePercentage} %
            </CardTitle>
            <CardDescription className="text-base">
              Všetky odpovede boli uložené do vašej histórie v{" "}
              <code>user_progress</code>.
            </CardDescription>
          </CardHeader>

          <CardContent>
            <div className="mx-auto grid max-w-xl grid-cols-3 gap-4 text-center">
              <div className="rounded-xl border bg-muted/30 p-4">
                <div className="text-2xl font-bold">{totalQuestions}</div>
                <div className="text-xs text-muted-foreground">
                  Celkovo otázok
                </div>
              </div>
              <div className="rounded-xl border border-emerald-500/30 bg-emerald-50/70 p-4 text-emerald-900">
                <div className="text-2xl font-bold">{correctCount}</div>
                <div className="text-xs">Správne</div>
              </div>
              <div className="rounded-xl border border-red-500/30 bg-red-50/70 p-4 text-red-900">
                <div className="text-2xl font-bold">{incorrectCount}</div>
                <div className="text-xs">Nesprávne</div>
              </div>
            </div>
          </CardContent>

          <CardFooter className="flex justify-center border-t pt-4">
            <Button onClick={handleResetToBuilder} size="lg">
              <RotateCcw className="h-4 w-4" />
              Vytvoriť nový test
            </Button>
          </CardFooter>
        </Card>

        {/* Prehľad všetkých otázok z testu s farebným označením (zelená/červená) a explanation */}
        <div className="space-y-4">
          <h2 className="text-xl font-bold tracking-tight">
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
                <CardHeader className="pb-3">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <span className="text-sm font-semibold text-muted-foreground">
                      Otázka #{idx + 1}
                    </span>
                    {item.isCorrect ? (
                      <Badge className="gap-1 bg-emerald-600 text-white hover:bg-emerald-600">
                        <CheckCircle2 className="h-3.5 w-3.5" />
                        Správne zodpovedané
                      </Badge>
                    ) : (
                      <Badge variant="destructive" className="gap-1">
                        <XCircle className="h-3.5 w-3.5" />
                        Nesprávne zodpovedané
                      </Badge>
                    )}
                  </div>
                  <CardTitle className="pt-1 text-lg leading-snug">
                    {item.content}
                  </CardTitle>
                </CardHeader>

                <CardContent className="space-y-4">
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
                          className={`flex items-center justify-between gap-3 rounded-lg border p-3 text-sm ${rowClass}`}
                        >
                          <div className="flex items-center gap-3">
                            <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded border bg-white/80 text-xs font-semibold uppercase">
                              {opt.id}
                            </span>
                            <span>{opt.text}</span>
                          </div>

                          <div className="flex shrink-0 items-center gap-2 text-xs">
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
                  <div className="rounded-lg border bg-card p-4 text-sm">
                    <div className="mb-1 flex items-center gap-1.5 font-semibold text-foreground">
                      <Sparkles className="h-4 w-4 text-primary" />
                      Vysvetlenie:
                    </div>
                    <p className="text-muted-foreground leading-relaxed">
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

