"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { createClient } from "@/utils/supabase/server";
import { isAdminEmail } from "@/lib/admin";

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

  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  if (error) {
    return { error: translateAuthError(error.message) };
  }

  // Ak prihlásený používateľ nie je administrátor, skontrolujeme schválenie
  const isAdmin = isAdminEmail(email);
  if (!isAdmin && data.user) {
    const { data: profile } = await supabase
      .from("profiles")
      .select("status")
      .eq("id", data.user.id)
      .maybeSingle();

    if (profile && profile.status !== "approved") {
      revalidatePath("/", "layout");
      redirect("/pending-approval");
    }
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

  // Zabezpečíme zápis do profiles so statusom 'pending' (alebo 'approved' pre admina)
  if (data.user) {
    try {
      await supabase.from("profiles").upsert({
        id: data.user.id,
        email: data.user.email ?? email,
        status: isAdminEmail(email) ? "approved" : "pending",
      });
    } catch {
      // Ignorovať, ak záznam vložil trigger
    }
  }

  // Ak je používateľ prihlásený, presmerujeme ho podľa stavu
  if (data.session) {
    revalidatePath("/", "layout");
    if (isAdminEmail(email)) {
      redirect("/admin");
    } else {
      redirect("/pending-approval");
    }
  }

  return {
    success:
      "Registrácia prebehla úspešne! Váš účet čaká na schválenie administrátorom (david.rusin). Hneď po schválení získate plný prístup.",
  };
}

export async function signOutAction() {
  const supabase = createClient();
  await supabase.auth.signOut();
  revalidatePath("/", "layout");
  redirect("/login");
}
