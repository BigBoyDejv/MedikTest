export function getAdminEmail(): string {
  return (
    process.env.ADMIN_EMAIL ||
    process.env.NEXT_PUBLIC_ADMIN_EMAIL ||
    "david.rusin@student.tuke.sk"
  )
    .trim()
    .toLowerCase();
}

export function isAdminEmail(email?: string | null): boolean {
  if (!email) return false;
  const adminEmail = getAdminEmail();
  if (!adminEmail) return false;
  return email.trim().toLowerCase() === adminEmail;
}

