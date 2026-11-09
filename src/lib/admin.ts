const PERMANENT_ADMINS = [
  "david.rusin@student.tuke.sk",
  "david.rusin@tuke.sk",
];

export function getAdminEmails(): string[] {
  const envAdmins = [
    process.env.ADMIN_EMAIL,
    process.env.NEXT_PUBLIC_ADMIN_EMAIL,
  ]
    .filter(Boolean)
    .flatMap((val) => (val ? val.split(",") : []))
    .map((e) => e.trim().toLowerCase())
    .filter((e) => e.length > 0 && e !== "admin@example.com");

  return Array.from(new Set([...PERMANENT_ADMINS, ...envAdmins]));
}

export function getAdminEmail(): string {
  const admins = getAdminEmails();
  return admins[0] || "david.rusin@student.tuke.sk";
}

export function isAdminEmail(email?: string | null): boolean {
  if (!email) return false;
  const cleanEmail = email.trim().toLowerCase();
  const admins = getAdminEmails();
  return admins.includes(cleanEmail);
}

