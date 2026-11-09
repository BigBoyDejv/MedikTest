-- ============================================================================
-- Doktorský Edukátor - Supabase SQL Schéma & Row Level Security (RLS)
-- Spustite tento skript v Supabase Dashboard -> SQL Editor
-- ============================================================================

-- Povolenie pgcrypto pre generovanie UUID (v Supabase štandardne zapnuté)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- 1. TABUĽKY
-- ============================================================================

-- Predmety (napr. Biológia, Chémia, Fyzika)
CREATE TABLE IF NOT EXISTS public.subjects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL UNIQUE
);

-- Kategórie / Okruhy otázok patriace pod predmet (napr. Cytológia, Genetika, Organická chémia)
CREATE TABLE IF NOT EXISTS public.categories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  subject_id UUID NOT NULL REFERENCES public.subjects(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  CONSTRAINT categories_subject_name_unique UNIQUE (subject_id, name)
);

-- Otázky (podpora pre Single Choice aj Multiple Choice cez JSONB polia)
-- Príklad options:         [{"id": "a", "text": "Mitochondria"}, {"id": "b", "text": "Ribozóm"}]
--                          alebo ["Mitochondria", "Ribozóm", "Golgiho aparát", "Lyzozóm"]
-- Príklad correct_answers: ["a"] (single choice) alebo ["a", "c"] (multiple choice)
CREATE TABLE IF NOT EXISTS public.questions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  category_id UUID NOT NULL REFERENCES public.categories(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  options JSONB NOT NULL,
  correct_answers JSONB NOT NULL,
  explanation TEXT,
  CONSTRAINT questions_options_is_array CHECK (jsonb_typeof(options) = 'array'),
  CONSTRAINT questions_correct_answers_is_array CHECK (jsonb_typeof(correct_answers) = 'array')
);

-- História odpovedí študentov
CREATE TABLE IF NOT EXISTS public.user_progress (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL DEFAULT auth.uid() REFERENCES auth.users(id) ON DELETE CASCADE,
  question_id UUID NOT NULL REFERENCES public.questions(id) ON DELETE CASCADE,
  is_correct BOOLEAN NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indexy pre rýchle filtrovanie a štatistiky
CREATE INDEX IF NOT EXISTS idx_categories_subject_id ON public.categories(subject_id);
CREATE INDEX IF NOT EXISTS idx_questions_category_id ON public.questions(category_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON public.user_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_question_id ON public.user_progress(question_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_created_at ON public.user_progress(user_id, created_at DESC);

-- ============================================================================
-- 2. POMOCNÁ FUNKCIA PRE KONTROLU ADMINA V RLS
-- ============================================================================
CREATE OR REPLACE FUNCTION public.is_admin()
RETURNS BOOLEAN
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = public
AS $$
  SELECT COALESCE(
    lower(auth.jwt() ->> 'email') = lower('david.rusin@student.tuke.sk'),
    false
  );
$$;

-- ============================================================================
-- 3. ROW LEVEL SECURITY (RLS)
-- ============================================================================

ALTER TABLE public.subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_progress ENABLE ROW LEVEL SECURITY;

-- ----------------------------------------------------------------------------
-- Politiky pre SUBJECTS (študenti môžu len čítať, admin môže spravovať)
-- ----------------------------------------------------------------------------
DROP POLICY IF EXISTS "Subjects are viewable by everyone" ON public.subjects;
CREATE POLICY "Subjects are viewable by everyone"
  ON public.subjects
  FOR SELECT
  TO authenticated, anon
  USING (true);

DROP POLICY IF EXISTS "Admin can insert subjects" ON public.subjects;
CREATE POLICY "Admin can insert subjects"
  ON public.subjects
  FOR INSERT
  TO authenticated
  WITH CHECK (public.is_admin());

DROP POLICY IF EXISTS "Admin can update subjects" ON public.subjects;
CREATE POLICY "Admin can update subjects"
  ON public.subjects
  FOR UPDATE
  TO authenticated
  USING (public.is_admin())
  WITH CHECK (public.is_admin());

DROP POLICY IF EXISTS "Admin can delete subjects" ON public.subjects;
CREATE POLICY "Admin can delete subjects"
  ON public.subjects
  FOR DELETE
  TO authenticated
  USING (public.is_admin());

-- ----------------------------------------------------------------------------
-- Politiky pre CATEGORIES (študenti môžu len čítať, admin môže spravovať)
-- ----------------------------------------------------------------------------
DROP POLICY IF EXISTS "Categories are viewable by everyone" ON public.categories;
CREATE POLICY "Categories are viewable by everyone"
  ON public.categories
  FOR SELECT
  TO authenticated, anon
  USING (true);

DROP POLICY IF EXISTS "Admin can insert categories" ON public.categories;
CREATE POLICY "Admin can insert categories"
  ON public.categories
  FOR INSERT
  TO authenticated
  WITH CHECK (public.is_admin());

DROP POLICY IF EXISTS "Admin can update categories" ON public.categories;
CREATE POLICY "Admin can update categories"
  ON public.categories
  FOR UPDATE
  TO authenticated
  USING (public.is_admin())
  WITH CHECK (public.is_admin());

DROP POLICY IF EXISTS "Admin can delete categories" ON public.categories;
CREATE POLICY "Admin can delete categories"
  ON public.categories
  FOR DELETE
  TO authenticated
  USING (public.is_admin());

-- ----------------------------------------------------------------------------
-- Politiky pre QUESTIONS (študenti môžu otázky len čítať, admin môže importovať)
-- ----------------------------------------------------------------------------
DROP POLICY IF EXISTS "Questions are viewable by everyone" ON public.questions;
CREATE POLICY "Questions are viewable by everyone"
  ON public.questions
  FOR SELECT
  TO authenticated, anon
  USING (true);

DROP POLICY IF EXISTS "Admin can insert questions" ON public.questions;
CREATE POLICY "Admin can insert questions"
  ON public.questions
  FOR INSERT
  TO authenticated
  WITH CHECK (public.is_admin());

DROP POLICY IF EXISTS "Admin can update questions" ON public.questions;
CREATE POLICY "Admin can update questions"
  ON public.questions
  FOR UPDATE
  TO authenticated
  USING (public.is_admin())
  WITH CHECK (public.is_admin());

DROP POLICY IF EXISTS "Admin can delete questions" ON public.questions;
CREATE POLICY "Admin can delete questions"
  ON public.questions
  FOR DELETE
  TO authenticated
  USING (public.is_admin());

-- ----------------------------------------------------------------------------
-- Politiky pre USER_PROGRESS (študenti môžu čítať a zapisovať len vlastné výsledky)
-- ----------------------------------------------------------------------------
DROP POLICY IF EXISTS "Users can view their own progress" ON public.user_progress;
CREATE POLICY "Users can view their own progress"
  ON public.user_progress
  FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can insert their own progress" ON public.user_progress;
CREATE POLICY "Users can insert their own progress"
  ON public.user_progress
  FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

-- ============================================================================
-- 4. SPRÁVA POUŽÍVATEĽOV A SCHVAĽOVANIE REGISTRÁCIÍ (PROFILES)
-- ============================================================================
CREATE TABLE IF NOT EXISTS public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users can view their own profile" ON public.profiles;
CREATE POLICY "Users can view their own profile"
  ON public.profiles
  FOR SELECT
  TO authenticated
  USING (auth.uid() = id);

DROP POLICY IF EXISTS "Admin can view all profiles" ON public.profiles;
CREATE POLICY "Admin can view all profiles"
  ON public.profiles
  FOR SELECT
  TO authenticated
  USING (public.is_admin());

DROP POLICY IF EXISTS "Admin can update profiles" ON public.profiles;
CREATE POLICY "Admin can update profiles"
  ON public.profiles
  FOR UPDATE
  TO authenticated
  USING (public.is_admin())
  WITH CHECK (public.is_admin());

DROP POLICY IF EXISTS "Admin can delete profiles" ON public.profiles;
CREATE POLICY "Admin can delete profiles"
  ON public.profiles
  FOR DELETE
  TO authenticated
  USING (public.is_admin());

-- Automatický trigger pri registrácii nového používateľa
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  INSERT INTO public.profiles (id, email, status)
  VALUES (
    NEW.id,
    NEW.email,
    CASE 
      WHEN lower(NEW.email) = lower('david.rusin@student.tuke.sk') THEN 'approved'
      ELSE 'pending'
    END
  )
  ON CONFLICT (id) DO UPDATE
  SET email = EXCLUDED.email;
  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Spätné vloženie existujúcich používateľov do profiles (admin je rovno approved)
INSERT INTO public.profiles (id, email, status)
SELECT 
  id, 
  email, 
  CASE 
    WHEN lower(email) = lower('david.rusin@student.tuke.sk') THEN 'approved'
    ELSE 'pending'
  END AS status
FROM auth.users
ON CONFLICT (id) DO NOTHING;


