"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { createClient } from "@/utils/supabase/server";

function isValidEmail(email: string): boolean {
  return /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email);
}

function translateAuthError(message: string): string {
  const lower = message.toLowerCase();
  if (lower.includes("invalid login credentials")) {
    return "Nesprávny e-mail alebo heslo.";
  }
  if (lower.includes("rate limit") || lower.includes("over_email_send_rate_limit")) {
    return "Prekročený limit odosielania potvrdzovacích e-mailov v Supabase. V administrácii Supabase (Authentication -> Providers -> Email) sa odporúča vypnúť voľbu 'Confirm email', aby sa dalo prihlasovať okamžite.";
  }
  if (lower.includes("user already registered") || lower.includes("already registered")) {
    return "Tento e-mail je už zaregistrovaný. Prejdite na prihlásenie pomocou vášho hesla.";
  }
  if (lower.includes("invalid format") || lower.includes("unable to validate email")) {
    return "Neplatný formát e-mailovej adresy. Uistite sa, že adresa neobsahuje diakritiku (dĺžne, mäkčene) ani medzery (napr. student@priklad.sk).";
  }
  if (lower.includes("password should be at least")) {
    return "Heslo musí obsahovať minimálne 6 znakov.";
  }
  return message;
}

export async function loginAction(formData: FormData) {
  const supabase = createClient();

  const email = String(formData.get("email") ?? "").trim().toLowerCase();
  const password = String(formData.get("password") ?? "");
  const nextPath = String(formData.get("next") ?? "/dashboard");

  if (!email || !password) {
    return { error: "Zadajte prosím e-mail aj heslo." };
  }

  if (!isValidEmail(email)) {
    return {
      error:
        "Neplatný formát e-mailu. Skontrolujte, či adresa neobsahuje mäkčene, dĺžne ani medzery.",
    };
  }

  const { error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  if (error) {
    return { error: translateAuthError(error.message) };
  }

  revalidatePath("/", "layout");
  redirect(nextPath.startsWith("/") ? nextPath : "/dashboard");
}

export async function signupAction(formData: FormData) {
  const supabase = createClient();

  const email = String(formData.get("email") ?? "").trim().toLowerCase();
  const password = String(formData.get("password") ?? "");

  if (!email || !isValidEmail(email)) {
    return {
      error:
        "Zadajte platnú e-mailovú adresu bez diakritiky (napr. student@gmail.com).",
    };
  }

  if (password.length < 6) {
    return {
      error: "Heslo musí mať minimálne 6 znakov.",
    };
  }

  const { data, error } = await supabase.auth.signUp({
    email,
    password,
  });

  if (error) {
    return { error: translateAuthError(error.message) };
  }

  // Ak už používateľ existuje, Supabase vracia prázdne identities pole
  if (
    data.user &&
    Array.isArray(data.user.identities) &&
    data.user.identities.length === 0
  ) {
    return {
      error:
        "Účet s týmto e-mailom už existuje! Prepnite sa hore na 'Prihlásenie' a zadajte svoje heslo.",
    };
  }

  // Ak je v Supabase vypnuté email confirmation, používateľ je rovno prihlásený
  if (data.session) {
    revalidatePath("/", "layout");
    redirect("/dashboard");
  }

  return {
    success:
      "Registrácia prebehla úspešne! Ak máte v Supabase zapnuté potvrdenie e-mailu, skontrolujte si schránku, alebo sa rovno prihláste.",
  };
}

export async function signOutAction() {
  const supabase = createClient();
  await supabase.auth.signOut();
  revalidatePath("/", "layout");
  redirect("/login");
}
