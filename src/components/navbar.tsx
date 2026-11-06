import Link from "next/link";
import { createClient } from "@/utils/supabase/server";
import { isAdminEmail } from "@/lib/admin";
import { signOutAction } from "@/app/login/actions";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  BarChart3,
  ClipboardList,
  GraduationCap,
  LogOut,
  ShieldCheck,
  User,
} from "lucide-react";

export async function Navbar() {
  const isConfigured = Boolean(
    process.env.NEXT_PUBLIC_SUPABASE_URL &&
      (process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY ||
        process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
  );

  let userEmail: string | null = null;

  if (isConfigured) {
    try {
      const supabase = createClient();
      const {
        data: { user },
      } = await supabase.auth.getUser();
      userEmail = user?.email ?? null;
    } catch {
      userEmail = null;
    }
  }

  const isAdmin = isAdminEmail(userEmail);

  return (
    <header className="sticky top-0 z-30 border-b bg-card/85 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6">
        <div className="flex items-center gap-6">
          <Link
            href={userEmail ? "/dashboard" : "/"}
            className="flex items-center gap-2.5 font-semibold tracking-tight text-foreground"
          >
            <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary text-primary-foreground">
              <GraduationCap className="h-5 w-5" />
            </span>
            <span>Doktorský Edukátor</span>
            <Badge variant="secondary" className="hidden sm:inline-flex">
              Bezplatná EdTech platforma
            </Badge>
          </Link>
        </div>

        <nav className="flex items-center gap-2.5">
          {userEmail && (
            <>
              <Button asChild variant="ghost" size="sm">
                <Link href="/dashboard">
                  <BarChart3 className="h-4 w-4 text-primary" />
                  <span>Dashboard</span>
                </Link>
              </Button>

              <Button asChild variant="default" size="sm">
                <Link href="/test">
                  <ClipboardList className="h-4 w-4" />
                  <span>Spustiť test</span>
                </Link>
              </Button>
            </>
          )}

          {isAdmin && (
            <Button asChild variant="outline" size="sm">
              <Link href="/admin">
                <ShieldCheck className="h-4 w-4 text-primary" />
                <span>Admin CMS</span>
              </Link>
            </Button>
          )}

          {userEmail ? (
            <div className="flex items-center gap-3">
              <div className="hidden items-center gap-1.5 text-sm text-muted-foreground md:flex">
                <User className="h-4 w-4" />
                <span>{userEmail}</span>
              </div>
              <form action={signOutAction}>
                <Button type="submit" variant="ghost" size="sm">
                  <LogOut className="h-4 w-4" />
                  <span>Odhlásiť</span>
                </Button>
              </form>
            </div>
          ) : (
            <Button asChild size="sm">
              <Link href="/login">Prihlásiť sa</Link>
            </Button>
          )}
        </nav>
      </div>
    </header>
  );
}
