"use client";

import * as React from "react";
import { recordQuestionProgressAction } from "@/app/actions";
import type { Question, QuestionOption } from "@/types/database";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { CheckCircle2, HelpCircle, XCircle } from "lucide-react";

function normalizeOptions(options: Question["options"]): QuestionOption[] {
  return options.map((opt, idx) => {
    if (typeof opt === "string") {
      return { id: opt, text: opt };
    }
    return {
      id: String(opt.id ?? idx),
      text: String(opt.text ?? ""),
    };
  });
}

export function PracticePreview({
  questions,
  isAuthenticated,
}: {
  questions: Question[];
  isAuthenticated: boolean;
}) {
  const [currentIndex, setCurrentIndex] = React.useState(0);
  const [selectedIds, setSelectedIds] = React.useState<string[]>([]);
  const [submitted, setSubmitted] = React.useState(false);
  const [saveNote, setSaveNote] = React.useState<string | null>(null);

  if (questions.length === 0) {
    return null;
  }

  const question = questions[currentIndex];
  const options = normalizeOptions(question.options);
  const correctSet = new Set(question.correct_answers.map(String));
  const isMultipleChoice = correctSet.size > 1;

  function toggleOption(optionId: string) {
    if (submitted) return;

    if (isMultipleChoice) {
      setSelectedIds((prev) =>
        prev.includes(optionId)
          ? prev.filter((id) => id !== optionId)
          : [...prev, optionId]
      );
    } else {
      setSelectedIds([optionId]);
    }
  }

  const isAnswerCorrect =
    selectedIds.length === correctSet.size &&
    selectedIds.every((id) => correctSet.has(id));

  async function handleCheckAnswer() {
    if (selectedIds.length === 0 || submitted) return;
    setSubmitted(true);
    setSaveNote(null);

    if (isAuthenticated) {
      const res = await recordQuestionProgressAction(
        question.id,
        isAnswerCorrect
      );
      if (res?.error) {
        setSaveNote(`Nepodarilo sa uložiť progres: ${res.error}`);
      } else {
        setSaveNote("Odpoveď bola uložená do vášho progresu (user_progress).");
      }
    } else {
      setSaveNote("Prihláste sa, aby sa vaše odpovede ukladali do histórie.");
    }
  }

  function handleNext() {
    setSelectedIds([]);
    setSubmitted(false);
    setSaveNote(null);
    setCurrentIndex((prev) => (prev + 1) % questions.length);
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center gap-2">
          <HelpCircle className="h-5 w-5 text-primary" />
          <CardTitle className="text-lg">
            Rýchle precvičovanie ({currentIndex + 1} / {questions.length})
          </CardTitle>
        </div>
        <CardDescription className="pt-2 text-base font-medium text-foreground">
          {question.content}
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-3">
        <div className="grid gap-2.5">
          {options.map((opt) => {
            const isSelected = selectedIds.includes(opt.id);
            const isCorrectOption = correctSet.has(opt.id);

            let borderStyle = "border-border hover:bg-accent/40";
            let badgeStyle = "border border-border bg-muted/60 text-muted-foreground";
            if (submitted) {
              if (isCorrectOption) {
                borderStyle =
                  "border-emerald-500 bg-emerald-950/30 text-emerald-200";
                badgeStyle = "bg-emerald-600 text-white border-emerald-600";
              } else if (isSelected && !isCorrectOption) {
                borderStyle = "border-destructive bg-destructive/20 text-destructive";
                badgeStyle = "bg-destructive text-white border-destructive";
              }
            } else if (isSelected) {
              borderStyle = "border-primary bg-primary/10 ring-1 ring-primary shadow-sm shadow-primary/20";
              badgeStyle = "bg-primary text-primary-foreground border-primary";
            }

            return (
              <button
                key={opt.id}
                type="button"
                onClick={() => toggleOption(opt.id)}
                className={`flex w-full items-center justify-between rounded-xl border p-3.5 text-left text-sm transition-all active:scale-[0.99] ${borderStyle}`}
              >
                <div className="flex items-center gap-3">
                  <span className={`flex h-6 w-6 shrink-0 items-center justify-center rounded text-xs font-semibold uppercase ${badgeStyle}`}>
                    {opt.id}
                  </span>
                  <span>{opt.text}</span>
                </div>
                {submitted && isCorrectOption && (
                  <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-400" />
                )}
                {submitted && isSelected && !isCorrectOption && (
                  <XCircle className="h-4 w-4 shrink-0 text-destructive" />
                )}
              </button>
            );
          })}
        </div>

        {submitted && (
          <div className="rounded-lg border bg-muted/40 p-4 text-sm space-y-1.5">
            <div className="font-semibold flex items-center gap-2">
              {isAnswerCorrect ? (
                <span className="text-emerald-700 flex items-center gap-1.5">
                  <CheckCircle2 className="h-4 w-4" /> Správna odpoveď!
                </span>
              ) : (
                <span className="text-destructive flex items-center gap-1.5">
                  <XCircle className="h-4 w-4" /> Nesprávna odpoveď
                </span>
              )}
            </div>
            {question.explanation && (
              <p className="text-muted-foreground">{question.explanation}</p>
            )}
            {saveNote && (
              <p className="text-xs text-muted-foreground pt-1">{saveNote}</p>
            )}
          </div>
        )}
      </CardContent>

      <CardFooter className="flex justify-between">
        {!submitted ? (
          <Button
            onClick={handleCheckAnswer}
            disabled={selectedIds.length === 0}
          >
            Overiť odpoveď
          </Button>
        ) : (
          <Button onClick={handleNext} variant="secondary">
            Ďalšia otázka →
          </Button>
        )}
      </CardFooter>
    </Card>
  );
}

