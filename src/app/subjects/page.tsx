import Link from "next/link";
import { createClient } from "@/utils/supabase/server";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ArrowRight, BookOpen, Layers } from "lucide-react";

export const dynamic = "force-dynamic";

export default async function SubjectsPage() {
  const isConfigured = Boolean(
    process.env.NEXT_PUBLIC_SUPABASE_URL && process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
  );

  if (!isConfigured) {
    return (
      <main className="mx-auto max-w-4xl px-4 py-12">
        <p className="text-muted-foreground">Supabase nie je nakonfigurovaný v .env.local</p>
      </main>
    );
  }

  const supabase = createClient();
  const [{ data: subjects }, { data: categories }] = await Promise.all([
    supabase.from("subjects").select("id, name").order("name"),
    supabase.from("categories").select("id, subject_id, name").order("name"),
  ]);

  return (
    <main className="mx-auto max-w-5xl space-y-8 px-4 py-8 sm:px-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Vyberte si predmet na precvičovanie</h1>
        <p className="mt-1 text-muted-foreground">
          Zvoľte si predmet a konkrétny tematický okruh otázok na prípravu na prijímacie skúšky.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {(subjects ?? []).map((subject) => {
          const subjectCategories = (categories ?? []).filter(
            (c) => c.subject_id === subject.id
          );

          return (
            <Card key={subject.id} className="flex flex-col justify-between">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
                      <BookOpen className="h-5 w-5" />
                    </div>
                    <div>
                      <CardTitle className="text-xl">{subject.name}</CardTitle>
                      <CardDescription>
                        {subjectCategories.length} tematických okruhov
                      </CardDescription>
                    </div>
                  </div>
                </div>
              </CardHeader>

              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                    Tematické okruhy
                  </span>
                  <div className="flex flex-wrap gap-2">
                    {subjectCategories.length > 0 ? (
                      subjectCategories.map((cat) => (
                        <Link
                          key={cat.id}
                          href={`/practice?category=${cat.id}`}
                          className="group inline-flex items-center gap-1.5 rounded-lg border bg-muted/40 px-3 py-1.5 text-xs font-medium transition hover:border-primary hover:bg-primary/5 hover:text-primary"
                        >
                          <Layers className="h-3 w-3 text-muted-foreground group-hover:text-primary" />
                          <span>{cat.name}</span>
                        </Link>
                      ))
                    ) : (
                      <span className="text-xs text-muted-foreground">
                        Zatiaľ žiadne kategórie
                      </span>
                    )}
                  </div>
                </div>

                <div className="pt-2">
                  <Button asChild className="w-full justify-between" size="sm">
                    <Link href={`/practice?subject=${subject.id}`}>
                      <span>Spustiť test zo všetkých okruhov ({subject.name})</span>
                      <ArrowRight className="h-4 w-4" />
                    </Link>
                  </Button>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </main>
  );
}

