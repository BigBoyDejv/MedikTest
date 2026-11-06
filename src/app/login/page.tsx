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
  const nextPath = searchParams.get("next") || "/";
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

      if (result?.error) {
        setError(result.error);
      } else if ("success" in (result || {}) && result?.success) {
        setSuccess(result.success);
      }
    } catch {
      // Redirect v server action vyhadzuje NEXT_REDIRECT, čo Next.js spracuje
    } finally {
      setIsPending(false);
    }
  }

  return (
    <div className="flex min-h-[calc(100vh-5rem)] items-center justify-center px-4 py-12">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-2 text-center">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary">
            <GraduationCap className="h-6 w-6" />
          </div>
          <CardTitle className="text-2xl font-bold">
            {mode === "login" ? "Prihlásenie do aplikácie" : "Vytvoriť študentský účet"}
          </CardTitle>
          <CardDescription>
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
              />
            </div>
          </CardContent>

          <CardFooter className="flex flex-col space-y-3">
            <Button type="submit" className="w-full" disabled={isPending}>
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

