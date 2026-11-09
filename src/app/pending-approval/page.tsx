import Link from "next/link";
import { redirect } from "next/navigation";
import { createClient } from "@/utils/supabase/server";
import { isAdminEmail } from "@/lib/admin";
import { signOutAction } from "@/app/login/actions";
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
import { Clock, GraduationCap, LogOut, RefreshCw, XCircle } from "lucide-react";

export const dynamic = "force-dynamic";

export default async function PendingApprovalPage() {
  const supabase = createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    redirect("/login");
  }

  // Admin má prístup vždy
  if (isAdminEmail(user.email)) {
    redirect("/admin");
  }

  const { data: profile } = await supabase
    .from("profiles")
    .select("status, created_at")
    .eq("id", user.id)
    .maybeSingle();

  const status = profile?.status ?? "pending";

  // Ak už bol schválený, pošleme ho na dashboard
  if (status === "approved") {
    redirect("/dashboard");
  }

  const isRejected = status === "rejected";

  return (
    <div className="flex min-h-[calc(100vh-5rem)] items-center justify-center px-4 py-12">
      <Card className="w-full max-w-lg border-amber-200/60 shadow-lg dark:border-amber-900/40">
        <CardHeader className="space-y-3 text-center">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-amber-100 text-amber-700 dark:bg-amber-950/60 dark:text-amber-400">
            {isRejected ? (
              <XCircle className="h-7 w-7 text-destructive" />
            ) : (
              <Clock className="h-7 w-7" />
            )}
          </div>

          <div className="space-y-1">
            <CardTitle className="text-2xl font-bold tracking-tight">
              {isRejected
                ? "Registrácia nebola schválená"
                : "Čaká sa na schválenie administrátorom"}
            </CardTitle>
            <CardDescription className="text-sm">
              Prihlásený e-mail:{" "}
              <strong className="text-foreground">{user.email}</strong>
            </CardDescription>
          </div>

          <div className="flex justify-center pt-1">
            <Badge
              variant={isRejected ? "destructive" : "secondary"}
              className="px-3 py-1 text-xs font-semibold"
            >
              {isRejected
                ? "Stav: Žiadosť zamietnutá"
                : "Stav: Čaká na posúdenie"}
            </Badge>
          </div>
        </CardHeader>

        <CardContent className="space-y-4 text-center text-sm text-muted-foreground">
          {isRejected ? (
            <p>
              Vaša žiadosť o registráciu bola administrátorom zamietnutá. V
              prípade otázok kontaktujte administrátora aplikácie.
            </p>
          ) : (
            <div className="space-y-2 rounded-lg bg-muted/50 p-4 text-left">
              <p className="font-medium text-foreground">Ako to funguje?</p>
              <ul className="list-inside list-disc space-y-1 text-xs sm:text-sm">
                <li>Váš účet bol úspešne vytvorený.</li>
                <li>
                  Administrátor aplikácie (<strong>david.rusin</strong>)
                  aktuálne eviduje vašu žiadosť vo svojej schvaľovacej tabuľke.
                </li>
                <li>
                  Hneď ako administrátor vašu žiadosť potvrdí, získate plný
                  prístup ku všetkým testovým otázkam a štatistikám.
                </li>
              </ul>
            </div>
          )}
        </CardContent>

        <CardFooter className="flex flex-col gap-2 sm:flex-row sm:justify-between">
          <form action={signOutAction} className="w-full sm:w-auto">
            <Button
              type="submit"
              variant="outline"
              size="sm"
              className="w-full gap-1.5"
            >
              <LogOut className="h-4 w-4" />
              Odhlásiť sa
            </Button>
          </form>

          {!isRejected && (
            <Button asChild size="sm" className="w-full sm:w-auto gap-1.5">
              <Link href="/pending-approval">
                <RefreshCw className="h-4 w-4" />
                Skontrolovať schválenie
              </Link>
            </Button>
          )}
        </CardFooter>
      </Card>
    </div>
  );
}
