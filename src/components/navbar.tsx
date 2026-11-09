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
    <header className="sticky top-0 z-40 border-b bg-card/90 backdrop-blur supports-[backdrop-filter]:bg-card/80">
      <div className="mx-auto flex h-14 max-w-6xl items-center justify-between gap-2 px-3 sm:h-16 sm:px-6">
        {/* Logo */}
        <Link
          href={userEmail ? "/dashboard" : "/"}
          className="flex min-w-0 items-center gap-2 font-semibold tracking-tight text-foreground sm:gap-2.5"
        >
          <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-primary text-primary-foreground sm:h-9 sm:w-9">
            <GraduationCap className="h-4 w-4 sm:h-5 sm:w-5" />
          </span>
          <span className="truncate text-sm sm:text-base">
            Doktorský Edukátor
          </span>
          <Badge variant="secondary" className="hidden lg:inline-flex">
            Bezplatná EdTech platforma
          </Badge>
        </Link>

        {/* Navigácia prispôsobená pre mobil, tablet aj desktop */}
        <nav className="flex shrink-0 items-center gap-1.5 sm:gap-2.5">
          {userEmail && (
            <>
              <Button
                asChild
                variant="ghost"
                size="sm"
                className="h-9 px-2.5 sm:px-3"
              >
                <Link href="/dashboard" title="Dashboard">
                  <BarChart3 className="h-4 w-4 text-primary" />
                  <span className="hidden sm:inline">Dashboard</span>
                </Link>
              </Button>

              <Button
                asChild
                variant="default"
                size="sm"
                className="h-9 px-2.5 sm:px-3"
              >
                <Link href="/test" title="Spustiť test">
                  <ClipboardList className="h-4 w-4" />
                  <span className="text-xs sm:text-sm">Test</span>
                </Link>
              </Button>
            </>
          )}

          {isAdmin && (
            <Button
              asChild
              variant="outline"
              size="sm"
              className="h-9 px-2.5 sm:px-3"
            >
              <Link href="/admin" title="Admin CMS">
                <ShieldCheck className="h-4 w-4 text-primary" />
                <span className="hidden md:inline">Admin CMS</span>
              </Link>
            </Button>
          )}

          {userEmail ? (
            <div className="flex items-center gap-1.5 sm:gap-2.5">
              <div className="hidden items-center gap-1.5 text-xs text-muted-foreground xl:flex">
                <User className="h-3.5 w-3.5" />
                <span className="max-w-[180px] truncate">{userEmail}</span>
              </div>
              <form action={signOutAction}>
                <Button
                  type="submit"
                  variant="ghost"
                  size="sm"
                  className="h-9 px-2 text-muted-foreground hover:text-foreground sm:px-3"
                  title="Odhlásiť sa"
                >
                  <LogOut className="h-4 w-4" />
                  <span className="hidden md:inline">Odhlásiť</span>
                </Button>
              </form>
            </div>
          ) : (
            <Button asChild size="sm" className="h-9">
              <Link href="/login">Prihlásiť sa</Link>
            </Button>
          )}
        </nav>
      </div>
    </header>
  );
}
