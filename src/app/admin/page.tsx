import { redirect } from "next/navigation";
import { createClient } from "@/utils/supabase/server";
import { isAdminEmail, getAdminEmail } from "@/lib/admin";
import { QuestionImportCms } from "@/components/admin/question-import-cms";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BookOpen, Database, Layers, ShieldCheck } from "lucide-react";

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

  // Načítanie prehľadu predmetov, kategórií a počtu otázok
  const [{ data: subjects }, { data: categories }, { count: questionsCount }] =
    await Promise.all([
      supabase.from("subjects").select("id, name").order("name"),
      supabase
        .from("categories")
        .select("id, subject_id, name")
        .order("name"),
      supabase.from("questions").select("id", { count: "exact", head: true }),
    ]);

  const subjectMap = new Map(
    (subjects ?? []).map((s) => [s.id, s.name] as const)
  );

  const formattedCategories = (categories ?? []).map((c) => ({
    id: c.id,
    name: c.name,
    subjectName: subjectMap.get(c.subject_id) ?? "Neznámy predmet",
  }));

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
              Prihlásený admin: {user.email}
            </span>
          </div>
          <h1 className="mt-2 text-3xl font-bold tracking-tight">
            Správa otázok a hromadný import
          </h1>
          <p className="text-sm text-muted-foreground">
            Importujte testové otázky vo formáte JSON priamo do Supabase databázy.
          </p>
        </div>
      </div>

      {/* Štatistické karty databázy */}
      <div className="grid gap-4 sm:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Predmety v databáze
            </CardTitle>
            <BookOpen className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{subjects?.length ?? 0}</div>
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
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Celkový počet otázok
            </CardTitle>
            <Database className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{questionsCount ?? 0}</div>
          </CardContent>
        </Card>
      </div>

      {/* Hlavný CMS komponent na hromadný import */}
      <QuestionImportCms categories={formattedCategories} />
    </main>
  );
}

