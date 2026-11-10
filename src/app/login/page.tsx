"use client";

import * as React from "react";
import { useSearchParams } from "next/navigation";
import { loginAction, signupAction } from "./actions";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AlertCircle, CheckCircle2, GraduationCap, Loader2 } from "lucide-react";

function LoginFormContent() {
  const searchParams = useSearchParams();
  const nextPath = searchParams.get("next") || "/dashboard";
  const urlError = searchParams.get("error");

  const [mode, setMode] = React.useState<"login" | "register">("login");
  const [error, setError] = React.useState<string | null>(urlError);
  const [success, setSuccess] = React.useState<string | null>(null);
  const [isPending, setIsPending] = React.useState(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setSuccess(null);
    setIsPending(true);

    const formData = new FormData(event.currentTarget);
    formData.set("next", nextPath);

    try {
      const result =
        mode === "login"
          ? await loginAction(formData)
          : await signupAction(formData);

      if (result && "error" in result && result.error) {
        setError(result.error);
      } else if (result && "success" in result && result.success) {
        setSuccess(result.success);
      }
    } catch {
      // Redirect v server action vyhadzuje NEXT_REDIRECT, čo Next.js spracuje
    } finally {
      setIsPending(false);
    }
  }

  return (
    <div className="relative flex min-h-[calc(100vh-5rem)] items-center justify-center px-4 py-12">
      <div className="pointer-events-none absolute h-96 w-96 rounded-full bg-primary/15 blur-3xl -top-10" />
      <Card className="relative z-10 w-full max-w-md border-border/80 shadow-2xl shadow-black/50">
        <CardHeader className="space-y-2 text-center">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10 text-primary border border-primary/20 shadow-sm shadow-primary/20">
            <GraduationCap className="h-7 w-7" />
          </div>
          <CardTitle className="text-2xl font-bold tracking-tight text-foreground">
            {mode === "login" ? "Prihlásenie do aplikácie" : "Vytvoriť študentský účet"}
          </CardTitle>
          <CardDescription className="text-muted-foreground text-sm">
            {mode === "login"
              ? "Prihláste sa pomocou e-mailu a hesla pre ukladanie vášho progresu."
              : "Bezplatná registrácia na precvičovanie otázok na prijímačky."}
          </CardDescription>
        </CardHeader>

        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4">
            {error && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Chyba</AlertTitle>
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {success && (
              <Alert variant="success">
                <CheckCircle2 className="h-4 w-4" />
                <AlertTitle>Hotovo</AlertTitle>
                <AlertDescription>{success}</AlertDescription>
              </Alert>
            )}

            <div className="space-y-2">
              <Label htmlFor="email">E-mailová adresa</Label>
              <Input
                id="email"
                name="email"
                type="email"
                placeholder="student@univerzita.sk"
                required
                autoComplete="email"
                className="bg-background/60 border-border/80 focus-visible:border-primary focus-visible:ring-primary"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Heslo</Label>
              <Input
                id="password"
                name="password"
                type="password"
                placeholder="••••••••"
                minLength={6}
                required
                autoComplete={
                  mode === "login" ? "current-password" : "new-password"
                }
                className="bg-background/60 border-border/80 focus-visible:border-primary focus-visible:ring-primary"
              />
            </div>
          </CardContent>

          <CardFooter className="flex flex-col space-y-3">
            <Button type="submit" className="w-full shadow-lg shadow-primary/30 font-semibold" disabled={isPending}>
              {isPending && <Loader2 className="h-4 w-4 animate-spin" />}
              {mode === "login" ? "Prihlásiť sa" : "Zaregistrovať sa"}
            </Button>

            <div className="text-center text-sm text-muted-foreground">
              {mode === "login" ? (
                <>
                  Ešte nemáte účet?{" "}
                  <button
                    type="button"
                    onClick={() => {
                      setMode("register");
                      setError(null);
                      setSuccess(null);
                    }}
                    className="font-medium text-primary underline-offset-4 hover:underline"
                  >
                    Zaregistrujte sa bezplatne
                  </button>
                </>
              ) : (
                <>
                  Už máte vytvorený účet?{" "}
                  <button
                    type="button"
                    onClick={() => {
                      setMode("login");
                      setError(null);
                      setSuccess(null);
                    }}
                    className="font-medium text-primary underline-offset-4 hover:underline"
                  >
                    Prihláste sa
                  </button>
                </>
              )}
            </div>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}

export default function LoginPage() {
  return (
    <React.Suspense fallback={<div className="p-8 text-center">Načítavam...</div>}>
      <LoginFormContent />
    </React.Suspense>
  );
}

