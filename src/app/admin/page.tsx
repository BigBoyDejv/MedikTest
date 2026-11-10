import { redirect } from "next/navigation";
import { createClient } from "@/utils/supabase/server";
import { isAdminEmail, getAdminEmail } from "@/lib/admin";
import { QuestionImportCms } from "@/components/admin/question-import-cms";
import {
  UserApprovalsCms,
  type UserProfileItem,
} from "@/components/admin/user-approvals-cms";
import {
  FlaggedQuestionsCms,
  type FlaggedQuestionItem,
} from "@/components/admin/flagged-questions-cms";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  BookOpen,
  Database,
  Flag,
  Layers,
  ShieldCheck,
  UserCheck,
} from "lucide-react";

export const dynamic = "force-dynamic";

export default async function AdminPage() {
  const supabase = createClient();

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    redirect("/login?next=/admin");
  }

  if (!isAdminEmail(user.email)) {
    return (
      <main className="mx-auto max-w-3xl px-4 py-16">
        <Card className="border-destructive/40">
          <CardHeader>
            <CardTitle className="text-destructive">
              403 – Prístup zamietnutý
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm text-muted-foreground">
            <p>
              Táto sekcia (<code>/admin</code>) je prístupná výhradne pre
              administrátorský e-mail definovaný v konfigurácii (
              <code>NEXT_PUBLIC_ADMIN_EMAIL</code> / <code>ADMIN_EMAIL</code>).
            </p>
            <p>
              Aktuálne prihlásený používateľ: <strong>{user.email}</strong>
            </p>
            {!getAdminEmail() && (
              <p className="text-amber-600">
                Upozornenie: V prostredí zatiaľ nie je nastavená premenná{" "}
                <code>NEXT_PUBLIC_ADMIN_EMAIL</code>.
              </p>
            )}
          </CardContent>
        </Card>
      </main>
    );
  }

  // Načítanie prehľadu predmetov, kategórií, počtu otázok, profilov a nahlásených otázok
  const [
    { data: subjects },
    { data: categories },
    { count: questionsCount },
    { data: profilesData },
    flaggedResult,
  ] = await Promise.all([
    supabase.from("subjects").select("id, name").order("name"),
    supabase.from("categories").select("id, subject_id, name").order("name"),
    supabase.from("questions").select("id", { count: "exact", head: true }),
    supabase
      .from("profiles")
      .select("id, email, status, created_at, updated_at")
      .order("created_at", { ascending: false }),
    supabase
      .from("flagged_questions")
      .select(
        `
        id,
        question_id,
        user_id,
        user_email,
        reason,
        status,
        created_at,
        resolved_at,
        question:questions(
          id,
          content,
          options,
          correct_answers,
          explanation,
          category:categories(
            name,
            subject:subjects(name)
          )
        )
      `
      )
      .order("created_at", { ascending: false }),
  ]);

  const flaggedQuestions: FlaggedQuestionItem[] = (
    flaggedResult.data || []
  ).map((f: any) => ({
    id: f.id,
    question_id: f.question_id,
    user_id: f.user_id,
    user_email: f.user_email,
    reason: f.reason,
    status: f.status,
    created_at: f.created_at,
    resolved_at: f.resolved_at,
    question: f.question,
  }));

  const tableMissing = Boolean(
    flaggedResult.error &&
      (flaggedResult.error.code === "42P01" ||
        flaggedResult.error.message.includes("does not exist"))
  );

  const pendingFlagsCount = flaggedQuestions.filter(
    (f) => f.status === "pending"
  ).length;

  const subjectMap = new Map(
    (subjects ?? []).map((s) => [s.id, s.name] as const)
  );

  const formattedCategories = (categories ?? []).map((c) => ({
    id: c.id,
    name: c.name,
    subjectName: subjectMap.get(c.subject_id) ?? "Neznámy predmet",
  }));

  const userProfiles: UserProfileItem[] = (profilesData ?? []).map((p) => ({
    id: p.id,
    email: p.email,
    status: (p.status as UserProfileItem["status"]) || "pending",
    created_at: p.created_at,
    updated_at: p.updated_at,
  }));

  const pendingApprovalsCount = userProfiles.filter(
    (u) => u.status === "pending"
  ).length;

  return (
    <main className="mx-auto max-w-6xl space-y-8 px-4 py-8 sm:px-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <Badge className="gap-1">
              <ShieldCheck className="h-3.5 w-3.5" />
              Admin CMS
            </Badge>
            <span className="text-xs text-muted-foreground">
              Prihlásený admin: <strong>{user.email}</strong>
            </span>
          </div>
          <h1 className="mt-2 text-3xl font-bold tracking-tight">
            Administrátorský panel
          </h1>
          <p className="text-sm text-muted-foreground">
            Správa používateľských prístupov a správa testových otázok.
          </p>
        </div>
      </div>

      {/* Štatistické karty */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
        <Card className={pendingFlagsCount > 0 ? "border-amber-500/50 bg-amber-500/5" : ""}>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-amber-500">
              Nahlásené otázky
            </CardTitle>
            <Flag className="h-4 w-4 text-amber-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-amber-500">
              {pendingFlagsCount}
            </div>
            <p className="text-xs text-muted-foreground mt-0.5">
              {pendingFlagsCount > 0 ? "Vyžadujú kontrolu" : "Všetko v poriadku"}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-amber-600 dark:text-amber-400">
              Čakajú na schválenie
            </CardTitle>
            <UserCheck className="h-4 w-4 text-amber-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-amber-600 dark:text-amber-400">
              {pendingApprovalsCount}
            </div>
            <p className="text-xs text-muted-foreground mt-0.5">Registrácie</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Predmety
            </CardTitle>
            <BookOpen className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{subjects?.length ?? 0}</div>
            <p className="text-xs text-muted-foreground mt-0.5">Aktívne predmety</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Kategórie (okruhy)
            </CardTitle>
            <Layers className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{categories?.length ?? 0}</div>
            <p className="text-xs text-muted-foreground mt-0.5">Tematické okruhy</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Otázky v databáze
            </CardTitle>
            <Database className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{questionsCount ?? 0}</div>
            <p className="text-xs text-muted-foreground mt-0.5">Spolu v systéme</p>
          </CardContent>
        </Card>
      </div>

      {/* 1. SEKCIA: Nahlásené otázky na kontrolu */}
      <section className="space-y-4">
        <FlaggedQuestionsCms
          initialFlagged={flaggedQuestions}
          tableMissing={tableMissing}
        />
      </section>

      {/* 2. SEKCIA: Schvaľovanie používateľov */}
      <section className="space-y-4 pt-4 border-t">
        <UserApprovalsCms initialProfiles={userProfiles} />
      </section>

      {/* 3. SEKCIA: Otázky a hromadný import */}
      <section className="space-y-4 pt-4 border-t">
        <h2 className="text-xl font-bold tracking-tight">
          Hromadný import a správa otázok
        </h2>
        <QuestionImportCms categories={formattedCategories} />
      </section>
    </main>
  );
}


