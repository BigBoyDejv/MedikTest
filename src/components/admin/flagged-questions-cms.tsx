"use client";

import * as React from "react";
import {
  updateFlaggedQuestionStatusAction,
  updateQuestionDetailsAction,
  deleteFlaggedQuestionAction,
} from "@/app/admin/actions";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import {
  AlertTriangle,
  CheckCircle2,
  Clock,
  Edit3,
  ExternalLink,
  Filter,
  Flag,
  Loader2,
  RefreshCw,
  Search,
  Trash2,
  X,
  XCircle,
} from "lucide-react";

export interface FlaggedQuestionItem {
  id: string;
  question_id: string;
  user_id: string | null;
  user_email: string | null;
  reason: string | null;
  status: "pending" | "resolved" | "dismissed";
  created_at: string;
  resolved_at: string | null;
  question?: {
    id: string;
    content: string;
    options: { id: string; text: string }[];
    correct_answers: string[];
    explanation: string | null;
    category?: {
      name: string;
      subject?: {
        name: string;
      };
    };
  } | null;
}

export function FlaggedQuestionsCms({
  initialFlagged,
  tableMissing = false,
}: {
  initialFlagged: FlaggedQuestionItem[];
  tableMissing?: boolean;
}) {
  const [flaggedList, setFlaggedList] =
    React.useState<FlaggedQuestionItem[]>(initialFlagged);
  const [search, setSearch] = React.useState("");
  const [filterStatus, setFilterStatus] = React.useState<
    "all" | "pending" | "resolved" | "dismissed"
  >("pending");
  const [actionLoadingId, setActionLoadingId] = React.useState<string | null>(
    null
  );
  const [actionMessage, setActionMessage] = React.useState<{
    type: "success" | "error";
    text: string;
  } | null>(null);

  // Stav pre modálne okno úpravy otázky
  const [editingItem, setEditingItem] =
    React.useState<FlaggedQuestionItem | null>(null);
  const [editContent, setEditContent] = React.useState("");
  const [editOptions, setEditOptions] = React.useState<
    { id: string; text: string }[]
  >([]);
  const [editCorrectAnswers, setEditCorrectAnswers] = React.useState<string[]>(
    []
  );
  const [editExplanation, setEditExplanation] = React.useState("");
  const [isSavingQuestion, setIsSavingQuestion] = React.useState(false);

  React.useEffect(() => {
    setFlaggedList(initialFlagged);
  }, [initialFlagged]);

  const filteredItems = React.useMemo(() => {
    return flaggedList.filter((item) => {
      if (filterStatus !== "all" && item.status !== filterStatus) {
        return false;
      }
      if (!search.trim()) return true;

      const q = search.toLowerCase();
      const questionText = item.question?.content.toLowerCase() || "";
      const reason = item.reason?.toLowerCase() || "";
      const email = item.user_email?.toLowerCase() || "";
      const categoryName = item.question?.category?.name.toLowerCase() || "";

      return (
        questionText.includes(q) ||
        reason.includes(q) ||
        email.includes(q) ||
        categoryName.includes(q)
      );
    });
  }, [flaggedList, filterStatus, search]);

  const pendingCount = React.useMemo(
    () => flaggedList.filter((f) => f.status === "pending").length,
    [flaggedList]
  );

  const handleUpdateStatus = async (
    flagId: string,
    newStatus: "pending" | "resolved" | "dismissed"
  ) => {
    setActionLoadingId(flagId);
    setActionMessage(null);

    const res = await updateFlaggedQuestionStatusAction(flagId, newStatus);
    setActionLoadingId(null);

    if (res.error) {
      setActionMessage({ type: "error", text: res.error });
    } else {
      setFlaggedList((prev) =>
        prev.map((f) =>
          f.id === flagId
            ? {
                ...f,
                status: newStatus,
                resolved_at:
                  newStatus !== "pending" ? new Date().toISOString() : null,
              }
            : f
        )
      );
      setActionMessage({
        type: "success",
        text: res.success ?? "Stav nahlásenia bol aktualizovaný.",
      });
    }
  };

  const handleDelete = async (flagId: string) => {
    if (!confirm("Naozaj chcete natrvalo odstrániť toto nahlásenie?")) return;

    setActionLoadingId(flagId);
    setActionMessage(null);

    const res = await deleteFlaggedQuestionAction(flagId);
    setActionLoadingId(null);

    if (res.error) {
      setActionMessage({ type: "error", text: res.error });
    } else {
      setFlaggedList((prev) => prev.filter((f) => f.id !== flagId));
      setActionMessage({
        type: "success",
        text: res.success ?? "Nahlásenie bolo odstránené.",
      });
    }
  };

  const openEditModal = (item: FlaggedQuestionItem) => {
    if (!item.question) return;
    setEditingItem(item);
    setEditContent(item.question.content);
    setEditOptions(item.question.options || []);
    setEditCorrectAnswers(item.question.correct_answers || []);
    setEditExplanation(item.question.explanation || "");
  };

  const handleSaveQuestion = async () => {
    if (!editingItem?.question) return;

    setIsSavingQuestion(true);
    setActionMessage(null);

    const res = await updateQuestionDetailsAction({
      questionId: editingItem.question.id,
      content: editContent,
      options: editOptions,
      correctAnswers: editCorrectAnswers,
      explanation: editExplanation,
      resolveFlagId: editingItem.id,
    });

    setIsSavingQuestion(false);

    if (res.error) {
      setActionMessage({ type: "error", text: res.error });
    } else {
      setFlaggedList((prev) =>
        prev.map((f) =>
          f.id === editingItem.id
            ? {
                ...f,
                status: "resolved",
                resolved_at: new Date().toISOString(),
                question: f.question
                  ? {
                      ...f.question,
                      content: editContent,
                      options: editOptions,
                      correct_answers: editCorrectAnswers,
                      explanation: editExplanation,
                    }
                  : null,
              }
            : f
        )
      );
      setEditingItem(null);
      setActionMessage({
        type: "success",
        text: res.success ?? "Otázka bola úspešne upravená.",
      });
    }
  };

  const toggleOptionCorrect = (optId: string) => {
    setEditCorrectAnswers((prev) =>
      prev.includes(optId)
        ? prev.filter((id) => id !== optId)
        : [...prev, optId].sort()
    );
  };

  return (
    <Card className="border-border">
      <CardHeader>
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <Badge variant="outline" className="gap-1 border-amber-500/40 text-amber-500 bg-amber-500/10">
                <Flag className="h-3.5 w-3.5" />
                Kontrola otázok
              </Badge>
              {pendingCount > 0 && (
                <Badge className="bg-amber-600 hover:bg-amber-600 text-white text-xs">
                  {pendingCount} vyžaduje pozornosť
                </Badge>
              )}
            </div>
            <CardTitle className="mt-2 text-2xl font-bold tracking-tight">
              Nahlásené otázky od študentov
            </CardTitle>
            <CardDescription className="text-sm">
              Otázky označené používateľmi počas testov alebo tréningu z dôvodu preklepov, chýb v kľúči alebo chýbajúcich vysvetlení.
            </CardDescription>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        {tableMissing && (
          <Alert className="border-amber-500/50 bg-amber-500/10 text-amber-200">
            <AlertTriangle className="h-4 w-4 text-amber-400" />
            <AlertTitle>Tabuľka nahlásení nebola vytvorená</AlertTitle>
            <AlertDescription className="text-xs space-y-2 mt-1">
              <p>
                Tabuľka <code>public.flagged_questions</code> ešte neexistuje v databáze Supabase.
                Pre aktiváciu spustite časť 5 zo súboru <code>supabase/schema.sql</code> v Supabase SQL Editori.
              </p>
            </AlertDescription>
          </Alert>
        )}

        {actionMessage && (
          <Alert
            variant={actionMessage.type === "error" ? "destructive" : "default"}
            className={
              actionMessage.type === "success"
                ? "border-emerald-500/40 bg-emerald-500/10 text-emerald-400"
                : ""
            }
          >
            {actionMessage.type === "success" ? (
              <CheckCircle2 className="h-4 w-4 text-emerald-400" />
            ) : (
              <AlertTriangle className="h-4 w-4 text-destructive" />
            )}
            <AlertDescription>{actionMessage.text}</AlertDescription>
          </Alert>
        )}

        {/* Vyhľadávanie a filtre */}
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Hľadať v texte otázky, dôvode nahlásenia alebo e-maile..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-9"
            />
          </div>

          <div className="flex flex-wrap items-center gap-1.5 border rounded-lg p-1 bg-muted/20">
            <Button
              type="button"
              variant={filterStatus === "pending" ? "default" : "ghost"}
              size="sm"
              onClick={() => setFilterStatus("pending")}
              className="text-xs gap-1.5"
            >
              <Clock className="h-3.5 w-3.5" />
              Čakajúce ({pendingCount})
            </Button>
            <Button
              type="button"
              variant={filterStatus === "resolved" ? "default" : "ghost"}
              size="sm"
              onClick={() => setFilterStatus("resolved")}
              className="text-xs gap-1.5"
            >
              <CheckCircle2 className="h-3.5 w-3.5" />
              Vyriešené (
              {flaggedList.filter((f) => f.status === "resolved").length})
            </Button>
            <Button
              type="button"
              variant={filterStatus === "dismissed" ? "default" : "ghost"}
              size="sm"
              onClick={() => setFilterStatus("dismissed")}
              className="text-xs gap-1.5"
            >
              <XCircle className="h-3.5 w-3.5" />
              Zamietnuté (
              {flaggedList.filter((f) => f.status === "dismissed").length})
            </Button>
            <Button
              type="button"
              variant={filterStatus === "all" ? "default" : "ghost"}
              size="sm"
              onClick={() => setFilterStatus("all")}
              className="text-xs"
            >
              Všetky ({flaggedList.length})
            </Button>
          </div>
        </div>

        {/* Zoznam nahlásených otázok */}
        {filteredItems.length === 0 ? (
          <div className="rounded-xl border border-dashed border-border p-8 text-center text-muted-foreground">
            <Flag className="mx-auto h-8 w-8 opacity-40 mb-2" />
            <p className="font-medium">
              {filterStatus === "pending"
                ? "Žiadne nahlásené otázky nečakajú na kontrolu."
                : "Nenašli sa žiadne nahlásenia zodpovedajúce filtru."}
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredItems.map((item) => {
              const q = item.question;
              const isPending = item.status === "pending";
              const isResolved = item.status === "resolved";

              return (
                <Card
                  key={item.id}
                  className={`overflow-hidden transition-all ${
                    isPending
                      ? "border-amber-500/40 bg-card shadow-sm shadow-amber-500/5"
                      : "border-border/60 bg-card/60 opacity-90"
                  }`}
                >
                  <CardHeader className="p-4 sm:p-5 border-b bg-muted/15">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                      <div className="space-y-1">
                        <div className="flex flex-wrap items-center gap-2">
                          <Badge
                            variant={
                              isPending
                                ? "destructive"
                                : isResolved
                                ? "default"
                                : "secondary"
                            }
                            className={`text-xs capitalize ${
                              isPending
                                ? "bg-amber-600 hover:bg-amber-600 text-white"
                                : isResolved
                                ? "bg-emerald-600 hover:bg-emerald-600 text-white"
                                : ""
                            }`}
                          >
                            {item.status === "pending"
                              ? "Vyžaduje kontrolu"
                              : item.status === "resolved"
                              ? "Vyriešené"
                              : "Zamietnuté"}
                          </Badge>
                          {q?.category?.subject?.name && (
                            <Badge variant="outline" className="text-xs">
                              {q.category.subject.name}
                            </Badge>
                          )}
                          {q?.category?.name && (
                            <span className="text-xs text-muted-foreground">
                              {q.category.name}
                            </span>
                          )}
                        </div>

                        <div className="text-xs text-muted-foreground pt-0.5">
                          Nahlásil:{" "}
                          <strong className="text-foreground">
                            {item.user_email || "Anonym"}
                          </strong>{" "}
                          • {new Date(item.created_at).toLocaleString("sk-SK")}
                        </div>
                      </div>

                      {/* Akčné tlačidlá */}
                      <div className="flex flex-wrap items-center gap-2">
                        {q && (
                          <Button
                            type="button"
                            variant="outline"
                            size="sm"
                            className="text-xs gap-1 border-primary/30 text-primary hover:bg-primary/10"
                            onClick={() => openEditModal(item)}
                          >
                            <Edit3 className="h-3.5 w-3.5" />
                            Upraviť otázku
                          </Button>
                        )}

                        {isPending && (
                          <>
                            <Button
                              type="button"
                              variant="outline"
                              size="sm"
                              className="text-xs gap-1 border-emerald-500/40 text-emerald-400 hover:bg-emerald-500/10"
                              onClick={() =>
                                handleUpdateStatus(item.id, "resolved")
                              }
                              disabled={actionLoadingId === item.id}
                            >
                              <CheckCircle2 className="h-3.5 w-3.5" />
                              Vyriešiť
                            </Button>
                            <Button
                              type="button"
                              variant="outline"
                              size="sm"
                              className="text-xs gap-1 border-border text-muted-foreground hover:bg-accent"
                              onClick={() =>
                                handleUpdateStatus(item.id, "dismissed")
                              }
                              disabled={actionLoadingId === item.id}
                            >
                              <X className="h-3.5 w-3.5" />
                              Zamietnuť
                            </Button>
                          </>
                        )}

                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          className="text-xs text-destructive hover:bg-destructive/10"
                          onClick={() => handleDelete(item.id)}
                          disabled={actionLoadingId === item.id}
                        >
                          <Trash2 className="h-3.5 w-3.5" />
                        </Button>
                      </div>
                    </div>
                  </CardHeader>

                  <CardContent className="p-4 sm:p-5 space-y-4">
                    {/* Dôvod nahlásenia */}
                    <div className="rounded-lg border border-amber-500/30 bg-amber-500/10 p-3 text-sm">
                      <div className="flex items-start gap-2">
                        <AlertTriangle className="h-4 w-4 shrink-0 text-amber-500 mt-0.5" />
                        <div>
                          <span className="font-semibold text-amber-500">
                            Dôvod nahlásenia:
                          </span>{" "}
                          <span className="text-foreground">
                            {item.reason || "Bez uvedenia detailov"}
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Otázka */}
                    {q ? (
                      <div className="space-y-3">
                        <h4 className="font-semibold text-base sm:text-lg">
                          {q.content}
                        </h4>

                        {/* Možnosti */}
                        <div className="grid gap-1.5 sm:grid-cols-2">
                          {q.options?.map((opt) => {
                            const isCorrect = q.correct_answers?.includes(
                              opt.id
                            );
                            return (
                              <div
                                key={opt.id}
                                className={`flex items-start gap-2 rounded-lg border p-2 text-xs sm:text-sm ${
                                  isCorrect
                                    ? "border-emerald-500/50 bg-emerald-500/10 font-medium text-emerald-300"
                                    : "border-border/50 bg-background/50 text-muted-foreground"
                                }`}
                              >
                                <span
                                  className={`flex h-5 w-5 shrink-0 items-center justify-center rounded text-xs font-bold ${
                                    isCorrect
                                      ? "bg-emerald-600 text-white"
                                      : "bg-muted text-muted-foreground"
                                  }`}
                                >
                                  {opt.id.toUpperCase()}
                                </span>
                                <span>{opt.text}</span>
                              </div>
                            );
                          })}
                        </div>

                        {/* Vysvetlenie */}
                        {q.explanation && (
                          <div className="rounded-lg border border-primary/20 bg-primary/5 p-3 text-xs sm:text-sm">
                            <span className="font-semibold text-primary">
                              Aktuálne vysvetlenie:
                            </span>{" "}
                            <span className="text-foreground/90">
                              {q.explanation}
                            </span>
                          </div>
                        )}
                      </div>
                    ) : (
                      <div className="text-xs text-muted-foreground italic">
                        Otázka bola v databáze zmazaná alebo sa nenašla.
                      </div>
                    )}
                  </CardContent>
                </Card>
              );
            })}
          </div>
        )}
      </CardContent>

      {/* Modálne okno / Dialóg pre priamu úpravu otázky */}
      {editingItem && editingItem.question && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4 backdrop-blur-sm animate-in fade-in">
          <div className="relative max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-2xl border border-border bg-card p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b pb-3">
              <div className="flex items-center gap-2">
                <Edit3 className="h-5 w-5 text-primary" />
                <h3 className="text-lg font-bold">Rýchla oprava otázky</h3>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setEditingItem(null)}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>

            <div className="space-y-4 text-sm">
              <div>
                <label className="text-xs font-semibold text-muted-foreground">
                  Znenie otázky:
                </label>
                <Textarea
                  value={editContent}
                  onChange={(e) => setEditContent(e.target.value)}
                  rows={2}
                  className="mt-1 font-medium"
                />
              </div>

              <div>
                <label className="text-xs font-semibold text-muted-foreground block mb-2">
                  Možnosti a správne odpovede (zaškrtnite správne):
                </label>
                <div className="space-y-2">
                  {editOptions.map((opt, idx) => {
                    const isCorrect = editCorrectAnswers.includes(opt.id);
                    return (
                      <div
                        key={opt.id}
                        className="flex items-center gap-2 rounded-lg border p-2"
                      >
                        <button
                          type="button"
                          onClick={() => toggleOptionCorrect(opt.id)}
                          className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-md font-bold text-xs transition-colors ${
                            isCorrect
                              ? "bg-emerald-600 text-white shadow-sm"
                              : "bg-muted text-muted-foreground hover:bg-muted/80"
                          }`}
                        >
                          {opt.id.toUpperCase()}
                        </button>
                        <Input
                          value={opt.text}
                          onChange={(e) => {
                            const newText = e.target.value;
                            setEditOptions((prev) =>
                              prev.map((o) =>
                                o.id === opt.id ? { ...o, text: newText } : o
                              )
                            );
                          }}
                          className="h-8 text-xs sm:text-sm"
                        />
                      </div>
                    );
                  })}
                </div>
              </div>

              <div>
                <label className="text-xs font-semibold text-muted-foreground">
                  Odborné vysvetlenie (prečo je to tak):
                </label>
                <Textarea
                  value={editExplanation}
                  onChange={(e) => setEditExplanation(e.target.value)}
                  rows={3}
                  className="mt-1 text-xs sm:text-sm"
                />
              </div>
            </div>

            <div className="flex items-center justify-end gap-2 border-t pt-4">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setEditingItem(null)}
                disabled={isSavingQuestion}
              >
                Zrušiť
              </Button>
              <Button
                size="sm"
                className="bg-primary hover:bg-brand-purple-hover text-primary-foreground font-semibold"
                onClick={handleSaveQuestion}
                disabled={isSavingQuestion}
              >
                {isSavingQuestion ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin mr-1.5" />
                    Ukladám zmeny...
                  </>
                ) : (
                  <>
                    <CheckCircle2 className="h-4 w-4 mr-1.5" />
                    Uložiť zmeny a vyriešiť nahlásenie
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>
      )}
    </Card>
  );
}
