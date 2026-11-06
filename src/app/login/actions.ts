"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { createClient } from "@/utils/supabase/server";

export async function loginAction(formData: FormData) {
  const supabase = createClient();

  const email = String(formData.get("email") ?? "").trim();
  const password = String(formData.get("password") ?? "");
  const nextPath = String(formData.get("next") ?? "/dashboard");

  if (!email || !password) {
    return { error: "Zadajte prosím e-mail aj heslo." };
  }

  const { error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  if (error) {
    return { error: error.message };
  }

  revalidatePath("/", "layout");
  redirect(nextPath.startsWith("/") ? nextPath : "/dashboard");
}

export async function signupAction(formData: FormData) {
  const supabase = createClient();

  const email = String(formData.get("email") ?? "").trim();
  const password = String(formData.get("password") ?? "");

  if (!email || password.length < 6) {
    return {
      error: "Zadajte platný e-mail a heslo (minimálne 6 znakov).",
    };
  }

  const { data, error } = await supabase.auth.signUp({
    email,
    password,
  });

  if (error) {
    return { error: error.message };
  }

  // Ak je v Supabase vypnuté email confirmation, používateľ je rovno prihlásený
  if (data.session) {
    revalidatePath("/", "layout");
    redirect("/dashboard");
  }

  return {
    success:
      "Registrácia prebehla úspešne! Skontrolujte si e-mailovú schránku pre potvrdenie účtu (alebo sa prihláste, ak je potvrdenie e-mailu vypnuté).",
  };
}

export async function signOutAction() {
  const supabase = createClient();
  await supabase.auth.signOut();
  revalidatePath("/", "layout");
  redirect("/login");
}
