# Doktorský Edukátor

Bezplatná EdTech aplikácia na prípravu na prijímacie skúšky (Next.js App Router, Tailwind CSS, shadcn/ui, Supabase Auth + Database).

## Rýchly štart (Fáza 1)

### 1. Inštalácia závislostí

```bash
npm install
```

### 2. Nastavenie Supabase databázy a RLS

1. Vytvorte nový projekt v [Supabase Dashboard](https://supabase.com/dashboard).
2. Otvorte **SQL Editor** a vložte obsah súboru [`supabase/schema.sql`](./supabase/schema.sql).
3. Vo funkcii `public.is_admin()` v `supabase/schema.sql` nahraďte `'admin@example.com'` svojím skutočným administrátorským e-mailom a skript spustite (**Run**).

### 3. Premenné prostredia (`.env.local`)

Skopírujte `.env.local.example` do `.env.local` a doplňte údaje zo Supabase (**Project Settings -> API**):

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_ADMIN_EMAIL=admin@example.com
ADMIN_EMAIL=admin@example.com
```

### 4. Spustenie vývojového servera

```bash
npm run dev
```

Aplikácia pobeží na `http://localhost:3000`:
- `/login` – prihlásenie a registrácia študentov cez e-mail a heslo (Supabase Auth).
- `/admin` – chránená administrátorská sekcia (prístupná len pre `ADMIN_EMAIL`) s hromadným JSON importom otázok do Supabase.

