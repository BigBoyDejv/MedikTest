import Link from "next/link";
import { createClient } from "@/utils/supabase/server";
import { isAdminEmail } from "@/lib/admin";
import { PracticePreview } from "@/components/practice-preview";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import {
  AlertTriangle,
  BookOpen,
  CheckCircle2,
  ClipboardList,
  ShieldCheck,
  Sparkles,
  Trophy,
} from "lucide-react";
import type { Question } from "@/types/database";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  const isSupabaseConfigured = Boolean(
    process.env.NEXT_PUBLIC_SUPABASE_URL &&
      (process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY ||
        process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
  );

  if (!isSupabaseConfigured) {
    return (
      <main className="mx-auto max-w-4xl space-y-6 px-4 py-12">
        <Alert>
          <AlertTriangle className="h-4 w-4" />
          <AlertTitle>Chýba konfigurácia Supabase (.env.local)</AlertTitle>
          <AlertDescription className="mt-2 space-y-2">
            <p>
              Pre prepojenie aplikácie so Supabase vytvorte súbor{" "}
              <code>.env.local</code> podľa vzoru <code>.env.local.example</code>.
            </p>
          </AlertDescription>
        </Alert>
      </main>
    );
  }

  const supabase = createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  const isAdmin = isAdminEmail(user?.email);

  const [{ data: subjects }, { data: categories }, { data: sampleQuestions }] =
    await Promise.all([
      supabase.from("subjects").select("id, name").order("name"),
      supabase.from("categories").select("id, subject_id, name").order("name"),
      supabase
        .from("questions")
        .select("id, category_id, content, options, correct_answers, explanation")
        .limit(20),
    ]);

  let totalAnswered = 0;
  let totalCorrect = 0;

  if (user) {
    const { data: progressRows } = await supabase
      .from("user_progress")
      .select("is_correct")
      .eq("user_id", user.id);

    totalAnswered = progressRows?.length ?? 0;
    totalCorrect = progressRows?.filter((r) => r.is_correct).length ?? 0;
  }

  const accuracy =
    totalAnswered > 0 ? Math.round((totalCorrect / totalAnswered) * 100) : 0;

  return (
    <main className="mx-auto max-w-6xl space-y-8 px-4 py-8 sm:px-6">
      {/* Hero sekcia */}
      <section className="rounded-2xl border bg-card p-6 shadow-sm sm:p-8">
        <div className="flex flex-col justify-between gap-6 md:flex-row md:items-center">
          <div className="space-y-2">
            <Badge variant="secondary" className="gap-1.5">
              <Sparkles className="h-3.5 w-3.5 text-primary" />
              100 % bezplatná príprava na prijímačky
            </Badge>
            <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
              Doktorský Edukátor
            </h1>
            <p className="max-w-2xl text-muted-foreground">
              Interaktívna databáza testových otázok (Single &amp; Multiple
              Choice) s konfigurátorom testov, okamžitým vysvetlením a sledovaním
              osobnej úspešnosti.
            </p>
          </div>

          <div className="flex flex-wrap gap-3">
            {user ? (
              <Button asChild size="lg">
                <Link href="/test">
                  <ClipboardList className="h-4 w-4" />
                  Konfigurátor testu (/test)
                </Link>
              </Button>
            ) : (
              <Button asChild size="lg">
                <Link href="/login">Prihlásiť sa / Registrovať</Link>
              </Button>
            )}
            {isAdmin && (
              <Button asChild variant="outline" size="lg">
                <Link href="/admin">
                  <ShieldCheck className="h-4 w-4 text-primary" />
                  Otvoriť Admin CMS
                </Link>
              </Button>
            )}
          </div>
        </div>
      </section>

      {/* Prehľad progresu prihláseného študenta */}
      <section className="grid gap-4 sm:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Zodpovedané otázky
            </CardTitle>
            <BookOpen className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalAnswered}</div>
            <p className="text-xs text-muted-foreground">
              {user
                ? "Uložené vo vašom profile"
                : "Prihláste sa pre sledovanie progresu"}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Správne odpovede
            </CardTitle>
            <CheckCircle2 className="h-4 w-4 text-emerald-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalCorrect}</div>
            <p className="text-xs text-muted-foreground">
              Celkový počet správnych pokusov
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Úspešnosť
            </CardTitle>
            <Trophy className="h-4 w-4 text-amber-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{accuracy} %</div>
            <p className="text-xs text-muted-foreground">
              Pomer správnych odpovedí
            </p>
          </CardContent>
        </Card>
      </section>

      {/* Precvičovanie otázok */}
      {sampleQuestions && sampleQuestions.length > 0 ? (
        <PracticePreview
          questions={sampleQuestions as Question[]}
          isAuthenticated={Boolean(user)}
        />
      ) : (
        <Card>
          <CardHeader>
            <CardTitle>Zatiaľ nie sú naimportované žiadne otázky</CardTitle>
            <CardDescription>
              Prihláste sa pomocou administrátorského e-mailu a v sekcii{" "}
              <Link href="/admin" className="font-medium text-primary underline">
                /admin
              </Link>{" "}
              nahrajte otázky cez hromadný JSON import.
            </CardDescription>
          </CardHeader>
        </Card>
      )}

      {/* Prehľad predmetov a kategórií */}
      <section className="space-y-4">
        <h2 className="text-xl font-semibold tracking-tight">
          Dostupné predmety a tematické okruhy
        </h2>
        <div className="grid gap-4 md:grid-cols-2">
          {(subjects ?? []).map((subject) => {
            const subjectCategories = (categories ?? []).filter(
              (c) => c.subject_id === subject.id
            );
            return (
              <Card key={subject.id}>
                <CardHeader>
                  <CardTitle className="text-lg">{subject.name}</CardTitle>
                  <CardDescription>
                    {subjectCategories.length} tematických okruhov
                  </CardDescription>
                </CardHeader>
                <CardContent className="flex flex-wrap gap-2">
                  {subjectCategories.length > 0 ? (
                    subjectCategories.map((cat) => (
                      <Link
                        key={cat.id}
                        href={`/test?category=${cat.id}`}
                        className="inline-flex"
                      >
                        <Badge
                          variant="secondary"
                          className="cursor-pointer hover:bg-primary hover:text-primary-foreground"
                        >
                          {cat.name}
                        </Badge>
                      </Link>
                    ))
                  ) : (
                    <span className="text-xs text-muted-foreground">
                      Zatiaľ bez kategórií
                    </span>
                  )}
                </CardContent>
              </Card>
            );
          })}
        </div>
      </section>
    </main>
  );
}
