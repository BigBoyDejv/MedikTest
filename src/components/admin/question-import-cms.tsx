"use client";

import * as React from "react";
import {
  createSubjectAndCategoryAction,
  importQuestionsFromJsonAction,
} from "@/app/admin/actions";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import {
  AlertCircle,
  CheckCircle2,
  FileJson,
  FolderPlus,
  Loader2,
  Sparkles,
  Upload,
} from "lucide-react";

interface CategoryOption {
  id: string;
  name: string;
  subjectName: string;
}

interface QuestionImportCmsProps {
  categories: CategoryOption[];
}

const SAMPLE_QUESTIONS_JSON = JSON.stringify(
  [
    {
      subject: "Biológia",
      category: "Cytológia a bunková biológia",
      content: "Ktorá bunková organela je hlavným miestom tvorby ATP pomocou oxidatívnej fosforylácie?",
      options: [
        { id: "a", text: "Mitochondria" },
        { id: "b", text: "Golgiho aparát" },
        { id: "c", text: "Lyzozóm" },
        { id: "d", text: "Drsné endoplazmatické retikulum" }
      ],
      correct_answers: ["a"],
      explanation: "Mitochondrie sú energetickým centrom eukaryotickej bunky – na vnútornej mitochondriálnej membráne prebieha dýchací reťazec a oxidatívna fosforylácia."
    },
    {
      subject: "Biológia",
      category: "Genetika",
      content: "Ktoré z nasledujúcich dusíkatých báz patria medzi purínové bázy prítomné v nukleových kyselinách (DNA a RNA)? (Multiple choice)",
      options: [
        { id: "a", text: "Adenín (A)" },
        { id: "b", text: "Cytuozín (C)" },
        { id: "c", text: "Guanín (G)" },
        { id: "d", text: "Tymín (T)" }
      ],
      correct_answers: ["a", "c"],
      explanation: "Purínové bázy majú dvojitý heterocyklus a patria sem adenín (A) a guanín (G). Cytozín, tymín a uracil sú pyrimidínové bázy."
    },
    {
      subject: "Chémia",
      category: "Všeobecná a anorganická chémia",
      content: "Aké je pH vodného roztoku silnej jednosýtnej kyseliny HCl s koncentráciou 0,001 mol/dm³ pri 25 °C?",
      options: [
        { id: "a", text: "pH = 1" },
        { id: "b", text: "pH = 2" },
        { id: "c", text: "pH = 3" },
        { id: "d", text: "pH = 4" }
      ],
      correct_answers: ["c"],
      explanation: "Pre úplne disociovanú HCl platí [H₃O⁺] = 10⁻³ mol/dm³, takže pH = -log(10⁻³) = 3."
    }
  ],
  null,
  2
);

export function QuestionImportCms({ categories }: QuestionImportCmsProps) {
  const [jsonText, setJsonText] = React.useState<string>("");
  const [selectedCategoryId, setSelectedCategoryId] = React.useState<string>(
    categories[0]?.id ?? ""
  );
  const [isImporting, setIsImporting] = React.useState(false);
  const [importError, setImportError] = React.useState<string | null>(null);
  const [importSuccess, setImportSuccess] = React.useState<string | null>(null);

  // Rýchle vytvorenie predmetu a kategórie
  const [newSubject, setNewSubject] = React.useState("");
  const [newCategory, setNewCategory] = React.useState("");
  const [isCreatingCat, setIsCreatingCat] = React.useState(false);
  const [catMessage, setCatMessage] = React.useState<{
    type: "success" | "error";
    text: string;
  } | null>(null);

  // Živá kontrola JSONu v prehliadači
  const jsonPreview = React.useMemo(() => {
    if (!jsonText.trim()) return null;
    try {
      const parsed = JSON.parse(jsonText);
      const arr = Array.isArray(parsed)
        ? parsed
        : parsed && Array.isArray(parsed.questions)
          ? parsed.questions
          : null;
      if (!arr) {
        return { valid: false, message: "JSON nie je pole otázok." };
      }
      const multiCount = arr.filter(
        (q: { correct_answers?: unknown[] }) =>
          Array.isArray(q?.correct_answers) && q.correct_answers.length > 1
      ).length;
      return {
        valid: true,
        total: arr.length,
        singleCount: arr.length - multiCount,
        multiCount,
      };
    } catch (e) {
      return {
        valid: false,
        message: e instanceof Error ? e.message : "Neplatný JSON",
      };
    }
  }, [jsonText]);

  async function handleImport(event: React.FormEvent) {
    event.preventDefault();
    setImportError(null);
    setImportSuccess(null);
    setIsImporting(true);

    try {
      const result = await importQuestionsFromJsonAction(
        jsonText,
        selectedCategoryId || undefined
      );

      if (result.error) {
        setImportError(result.error);
      } else if (result.success) {
        setImportSuccess(result.success);
        setJsonText("");
      }
    } finally {
      setIsImporting(false);
    }
  }

  async function handleCreateCategory(event: React.FormEvent) {
    event.preventDefault();
    setCatMessage(null);
    setIsCreatingCat(true);

    try {
      const result = await createSubjectAndCategoryAction(
        newSubject,
        newCategory
      );
      if (result.error) {
        setCatMessage({ type: "error", text: result.error });
      } else if (result.success) {
        setCatMessage({ type: "success", text: result.success });
        if (result.categoryId) {
          setSelectedCategoryId(result.categoryId);
        }
        setNewCategory("");
      }
    } finally {
      setIsCreatingCat(false);
    }
  }

  return (
    <div className="grid gap-6 lg:grid-cols-3">
      {/* Hlavný stĺpec: Hromadný JSON import */}
      <Card className="lg:col-span-2">
        <CardHeader>
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div>
              <CardTitle className="flex items-center gap-2">
                <FileJson className="h-5 w-5 text-primary" />
                Hromadný import otázok (JSON)
              </CardTitle>
              <CardDescription className="mt-1">
                Vložte JSON pole otázok (single alebo multiple choice) a kliknite
                na <strong>Importovať</strong> pre uloženie do Supabase.
              </CardDescription>
            </div>

            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => {
                setJsonText(SAMPLE_QUESTIONS_JSON);
                setImportError(null);
                setImportSuccess(null);
              }}
            >
              <Sparkles className="h-4 w-4 text-primary" />
              Vložiť ukážkový JSON
            </Button>
          </div>
        </CardHeader>

        <form onSubmit={handleImport}>
          <CardContent className="space-y-4">
            {importError && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Chyba pri importe</AlertTitle>
                <AlertDescription>{importError}</AlertDescription>
              </Alert>
            )}

            {importSuccess && (
              <Alert variant="success">
                <CheckCircle2 className="h-4 w-4" />
                <AlertTitle>Import dokončený</AlertTitle>
                <AlertDescription>{importSuccess}</AlertDescription>
              </Alert>
            )}

            <div className="space-y-2">
              <Label htmlFor="defaultCategory">
                Predvolená kategória (voliteľné, ak je v JSONe uvedený{" "}
                <code className="rounded bg-muted px-1 py-0.5 text-xs">
                  subject
                </code>{" "}
                a{" "}
                <code className="rounded bg-muted px-1 py-0.5 text-xs">
                  category
                </code>
                )
              </Label>
              <select
                id="defaultCategory"
                value={selectedCategoryId}
                onChange={(e) => setSelectedCategoryId(e.target.value)}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              >
                <option value="">
                  -- Automaticky podľa &quot;subject&quot; a &quot;category&quot; v JSONe --
                </option>
                {categories.map((cat) => (
                  <option key={cat.id} value={cat.id}>
                    {cat.subjectName} → {cat.name} ({cat.id.slice(0, 8)}…)
                  </option>
                ))}
              </select>
            </div>

            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label htmlFor="questionsJson">JSON dáta otázok</Label>
                {jsonPreview && (
                  <div className="flex items-center gap-2 text-xs">
                    {jsonPreview.valid ? (
                      <>
                        <Badge variant="secondary">
                          {jsonPreview.total} otázok pripravených
                        </Badge>
                        <Badge variant="outline">
                          Single: {jsonPreview.singleCount} | Multiple:{" "}
                          {jsonPreview.multiCount}
                        </Badge>
                      </>
                    ) : (
                      <Badge variant="destructive">
                        Neplatný JSON: {jsonPreview.message}
                      </Badge>
                    )}
                  </div>
                )}
              </div>

              <Textarea
                id="questionsJson"
                value={jsonText}
                onChange={(e) => setJsonText(e.target.value)}
                placeholder={`[\n  {\n    "subject": "Biológia",\n    "category": "Cytológia",\n    "content": "Text otázky...",\n    "options": [\n      { "id": "a", "text": "Možnosť A" },\n      { "id": "b", "text": "Možnosť B" }\n    ],\n    "correct_answers": ["a"],\n    "explanation": "Vysvetlenie správnej odpovede..."\n  }\n]`}
                className="min-h-[340px] font-mono text-xs leading-relaxed"
                required
              />
            </div>
          </CardContent>

          <CardFooter className="flex items-center justify-between gap-4 border-t pt-4">
            <p className="text-xs text-muted-foreground">
              Podporuje Single Choice (1 prvok v{" "}
              <code>correct_answers</code>) aj Multiple Choice (viac prvkov v{" "}
              <code>correct_answers</code>).
            </p>
            <Button
              type="submit"
              disabled={isImporting || !jsonText.trim()}
              className="min-w-[150px]"
            >
              {isImporting ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Importujem...
                </>
              ) : (
                <>
                  <Upload className="h-4 w-4" />
                  Importovať
                </>
              )}
            </Button>
          </CardFooter>
        </form>
      </Card>

      {/* Bočný stĺpec: Rýchle pridanie predmetu/kategórie + Nápoveda k JSON schéme */}
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <FolderPlus className="h-4 w-4 text-primary" />
              Vytvoriť predmet a kategóriu
            </CardTitle>
            <CardDescription>
              Rýchle vytvorenie nového predmetu a okruhu otázok v databáze.
            </CardDescription>
          </CardHeader>

          <form onSubmit={handleCreateCategory}>
            <CardContent className="space-y-3">
              {catMessage && (
                <Alert
                  variant={
                    catMessage.type === "error" ? "destructive" : "success"
                  }
                >
                  <AlertDescription>{catMessage.text}</AlertDescription>
                </Alert>
              )}

              <div className="space-y-1.5">
                <Label htmlFor="subjectName">Predmet</Label>
                <Input
                  id="subjectName"
                  placeholder="napr. Biológia"
                  value={newSubject}
                  onChange={(e) => setNewSubject(e.target.value)}
                  required
                />
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="categoryName">Kategória / Okruh</Label>
                <Input
                  id="categoryName"
                  placeholder="napr. Genetika"
                  value={newCategory}
                  onChange={(e) => setNewCategory(e.target.value)}
                  required
                />
              </div>
            </CardContent>

            <CardFooter>
              <Button
                type="submit"
                variant="secondary"
                className="w-full"
                disabled={isCreatingCat}
              >
                {isCreatingCat && <Loader2 className="h-4 w-4 animate-spin" />}
                Uložiť kategóriu
              </Button>
            </CardFooter>
          </form>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">Štruktúra JSON položky</CardTitle>
            <CardDescription>
              Každá otázka v poli môže obsahovať nasledovné polia:
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-2 text-xs text-muted-foreground">
            <div>
              <code className="font-semibold text-foreground">
                subject + category
              </code>{" "}
              (alebo{" "}
              <code className="font-semibold text-foreground">category_id</code>
              ): názov predmetu a kategórie (automaticky sa vytvoria, ak ešte
              neexistujú).
            </div>
            <div>
              <code className="font-semibold text-foreground">content</code>{" "}
              (string): znenie otázky.
            </div>
            <div>
              <code className="font-semibold text-foreground">options</code>{" "}
              (JSONB pole): napr.{" "}
              <code>{`[{"id": "a", "text": "..."}, ...]`}</code>.
            </div>
            <div>
              <code className="font-semibold text-foreground">
                correct_answers
              </code>{" "}
              (JSONB pole): napr. <code>{`["a"]`}</code> pre single choice alebo{" "}
              <code>{`["a", "c"]`}</code> pre multiple choice.
            </div>
            <div>
              <code className="font-semibold text-foreground">explanation</code>{" "}
              (string, voliteľné): vysvetlenie správnej odpovede po vyhodnotení.
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

