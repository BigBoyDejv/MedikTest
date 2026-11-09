"use client";

import * as React from "react";
import {
  updateUserApprovalStatusAction,
  deleteUserProfileAction,
} from "@/app/admin/actions";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import {
  CheckCircle2,
  Clock,
  Filter,
  Loader2,
  RotateCcw,
  Search,
  ShieldCheck,
  UserCheck,
  Users,
  UserX,
  XCircle,
} from "lucide-react";

export interface UserProfileItem {
  id: string;
  email: string;
  status: "pending" | "approved" | "rejected";
  created_at: string;
  updated_at?: string;
}

export function UserApprovalsCms({
  initialProfiles,
}: {
  initialProfiles: UserProfileItem[];
}) {
  const [profiles, setProfiles] = React.useState<UserProfileItem[]>(initialProfiles);
  const [search, setSearch] = React.useState("");
  const [filterStatus, setFilterStatus] = React.useState<
    "all" | "pending" | "approved" | "rejected"
  >("all");
  const [pendingId, setPendingId] = React.useState<string | null>(null);
  const [actionMessage, setActionMessage] = React.useState<{
    type: "success" | "error";
    text: string;
  } | null>(null);

  // Synchronizácia props ak dôjde k revalidácii
  React.useEffect(() => {
    setProfiles(initialProfiles);
  }, [initialProfiles]);

  const pendingCount = profiles.filter((p) => p.status === "pending").length;
  const approvedCount = profiles.filter((p) => p.status === "approved").length;
  const rejectedCount = profiles.filter((p) => p.status === "rejected").length;

  const filtered = profiles.filter((p) => {
    const matchesSearch = p.email
      .toLowerCase()
      .includes(search.trim().toLowerCase());
    const matchesFilter =
      filterStatus === "all" ? true : p.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  async function handleStatusChange(
    userId: string,
    newStatus: "approved" | "rejected" | "pending"
  ) {
    setPendingId(userId);
    setActionMessage(null);

    const res = await updateUserApprovalStatusAction(userId, newStatus);
    setPendingId(null);

    if (res?.error) {
      setActionMessage({ type: "error", text: res.error });
    } else {
      setActionMessage({
        type: "success",
        text: res.success || "Stav bol úspešne zmenený.",
      });
      setProfiles((prev) =>
        prev.map((p) => (p.id === userId ? { ...p, status: newStatus } : p))
      );
    }
  }

  function formatDate(isoString: string): string {
    try {
      const date = new Date(isoString);
      return date.toLocaleString("sk-SK", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch {
      return isoString;
    }
  }

  return (
    <div className="space-y-6">
      {/* Prehľadové karty */}
      <div className="grid gap-3 sm:grid-cols-4">
        <Card
          className={`cursor-pointer transition-colors ${
            filterStatus === "all" ? "ring-2 ring-primary" : "hover:bg-muted/40"
          }`}
          onClick={() => setFilterStatus("all")}
        >
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-xs font-medium text-muted-foreground">
              Všetci používatelia
            </CardTitle>
            <Users className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{profiles.length}</div>
          </CardContent>
        </Card>

        <Card
          className={`cursor-pointer transition-colors ${
            filterStatus === "pending"
              ? "ring-2 ring-amber-500"
              : "hover:bg-muted/40"
          }`}
          onClick={() => setFilterStatus("pending")}
        >
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-xs font-medium text-amber-600 dark:text-amber-400">
              Čakajú na schválenie
            </CardTitle>
            <Clock className="h-4 w-4 text-amber-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-amber-600 dark:text-amber-400">
              {pendingCount}
            </div>
          </CardContent>
        </Card>

        <Card
          className={`cursor-pointer transition-colors ${
            filterStatus === "approved"
              ? "ring-2 ring-emerald-500"
              : "hover:bg-muted/40"
          }`}
          onClick={() => setFilterStatus("approved")}
        >
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-xs font-medium text-emerald-600 dark:text-emerald-400">
              Schválení študenti
            </CardTitle>
            <UserCheck className="h-4 w-4 text-emerald-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">
              {approvedCount}
            </div>
          </CardContent>
        </Card>

        <Card
          className={`cursor-pointer transition-colors ${
            filterStatus === "rejected"
              ? "ring-2 ring-destructive"
              : "hover:bg-muted/40"
          }`}
          onClick={() => setFilterStatus("rejected")}
        >
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-xs font-medium text-destructive">
              Zamietnutí
            </CardTitle>
            <UserX className="h-4 w-4 text-destructive" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-destructive">
              {rejectedCount}
            </div>
          </CardContent>
        </Card>
      </div>

      {actionMessage && (
        <Alert
          variant={actionMessage.type === "error" ? "destructive" : "default"}
          className={
            actionMessage.type === "success"
              ? "border-emerald-500 text-emerald-700 dark:text-emerald-300"
              : ""
          }
        >
          {actionMessage.type === "success" ? (
            <CheckCircle2 className="h-4 w-4 text-emerald-600" />
          ) : (
            <XCircle className="h-4 w-4" />
          )}
          <AlertTitle>
            {actionMessage.type === "success" ? "Úspech" : "Chyba"}
          </AlertTitle>
          <AlertDescription>{actionMessage.text}</AlertDescription>
        </Alert>
      )}

      {/* Tabuľka so schvaľovaním */}
      <Card>
        <CardHeader>
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <CardTitle className="text-lg font-bold">
                Schvaľovanie prístupov používateľov
              </CardTitle>
              <CardDescription>
                Študenti získajú prístup k testovacím okruhom až po tom, čo ich
                žiadosť schváliš.
              </CardDescription>
            </div>

            {/* Vyhľadávanie */}
            <div className="relative w-full sm:w-64">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                type="text"
                placeholder="Hľadať e-mail..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-9 h-9"
              />
            </div>
          </div>
        </CardHeader>

        <CardContent>
          {filtered.length === 0 ? (
            <div className="py-12 text-center text-sm text-muted-foreground">
              {search
                ? "Nenašiel sa žiadny používateľ vyhovujúci vyhľadávaniu."
                : filterStatus === "pending"
                ? "Žiadni používatelia momentálne nečakajú na schválenie."
                : "V databáze sa nenachádzajú žiadne záznamy."}
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="border-b text-xs uppercase text-muted-foreground">
                    <th className="py-3 px-3 font-semibold">E-mail študenta</th>
                    <th className="py-3 px-3 font-semibold">Dátum registrácie</th>
                    <th className="py-3 px-3 font-semibold">Aktuálny stav</th>
                    <th className="py-3 px-3 text-right font-semibold">
                      Schvaľovacie akcie
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {filtered.map((profile) => {
                    const isRowPending = pendingId === profile.id;
                    const isSelfAdmin =
                      profile.email.toLowerCase() ===
                      "david.rusin@student.tuke.sk";

                    return (
                      <tr
                        key={profile.id}
                        className="hover:bg-muted/40 transition-colors"
                      >
                        <td className="py-3.5 px-3 font-medium">
                          <div className="flex items-center gap-2">
                            <span>{profile.email}</span>
                            {isSelfAdmin && (
                              <Badge
                                variant="outline"
                                className="border-primary text-primary text-[10px] uppercase font-bold"
                              >
                                Váš Admin Účet
                              </Badge>
                            )}
                          </div>
                        </td>

                        <td className="py-3.5 px-3 text-muted-foreground text-xs">
                          {formatDate(profile.created_at)}
                        </td>

                        <td className="py-3.5 px-3">
                          {profile.status === "approved" && (
                            <Badge
                              variant="default"
                              className="bg-emerald-600 hover:bg-emerald-600 text-white gap-1 text-xs"
                            >
                              <CheckCircle2 className="h-3 w-3" />
                              Schválený
                            </Badge>
                          )}
                          {profile.status === "pending" && (
                            <Badge
                              variant="secondary"
                              className="bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 gap-1 text-xs font-semibold"
                            >
                              <Clock className="h-3 w-3" />
                              Čaká na schválenie
                            </Badge>
                          )}
                          {profile.status === "rejected" && (
                            <Badge
                              variant="destructive"
                              className="gap-1 text-xs"
                            >
                              <XCircle className="h-3 w-3" />
                              Zamietnutý
                            </Badge>
                          )}
                        </td>

                        <td className="py-3.5 px-3 text-right">
                          {isSelfAdmin ? (
                            <span className="text-xs text-muted-foreground italic">
                              Hlavný administrátor
                            </span>
                          ) : (
                            <div className="flex items-center justify-end gap-1.5">
                              {profile.status !== "approved" && (
                                <Button
                                  size="sm"
                                  variant="default"
                                  className="h-8 bg-emerald-600 hover:bg-emerald-700 text-white gap-1 px-3"
                                  disabled={isRowPending}
                                  onClick={() =>
                                    handleStatusChange(profile.id, "approved")
                                  }
                                >
                                  {isRowPending ? (
                                    <Loader2 className="h-3.5 w-3.5 animate-spin" />
                                  ) : (
                                    <CheckCircle2 className="h-3.5 w-3.5" />
                                  )}
                                  <span>Schváliť</span>
                                </Button>
                              )}

                              {profile.status !== "rejected" && (
                                <Button
                                  size="sm"
                                  variant="outline"
                                  className="h-8 text-destructive hover:bg-destructive hover:text-destructive-foreground gap-1 px-2.5"
                                  disabled={isRowPending}
                                  onClick={() =>
                                    handleStatusChange(profile.id, "rejected")
                                  }
                                >
                                  {isRowPending ? (
                                    <Loader2 className="h-3.5 w-3.5 animate-spin" />
                                  ) : (
                                    <XCircle className="h-3.5 w-3.5" />
                                  )}
                                  <span>Zamietnuť</span>
                                </Button>
                              )}

                              {profile.status !== "pending" && (
                                <Button
                                  size="sm"
                                  variant="ghost"
                                  className="h-8 text-muted-foreground gap-1 px-2"
                                  title="Vrátiť do čakajúcich"
                                  disabled={isRowPending}
                                  onClick={() =>
                                    handleStatusChange(profile.id, "pending")
                                  }
                                >
                                  <RotateCcw className="h-3.5 w-3.5" />
                                </Button>
                              )}
                            </div>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
