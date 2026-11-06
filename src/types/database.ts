export interface Subject {
  id: string;
  name: string;
}

export interface Category {
  id: string;
  subject_id: string;
  name: string;
}

export interface QuestionOption {
  id: string;
  text: string;
}

/**
 * Podporujeme 2 formáty v stĺpci `options` (JSONB):
 * 1) Pole objektov: [{ "id": "a", "text": "Mitochondria" }, ...]
 * 2) Pole stringov: ["Mitochondria", "Ribozóm", ...] (vtedy sú kľúče odpovedí buď texty alebo indexy/písmená)
 */
export type RawQuestionOption = QuestionOption | string;

export interface Question {
  id: string;
  category_id: string;
  content: string;
  options: RawQuestionOption[];
  correct_answers: string[];
  explanation: string | null;
}

export interface UserProgress {
  id: string;
  user_id: string;
  question_id: string;
  is_correct: boolean;
  created_at: string;
}

/**
 * Schéma jednej položky pre hromadný JSON import v /admin CMS.
 * Admin môže buď zadať `category_id` priamo, alebo zadať `subject` + `category`
 * (CMS automaticky nájde alebo vytvorí daný predmet a kategóriu),
 * prípadne vybrať cieľovú kategóriu v rozhraní.
 */
export interface BulkImportQuestionItem {
  category_id?: string;
  subject?: string;
  category?: string;
  content: string;
  options: RawQuestionOption[];
  correct_answers: string[];
  explanation?: string | null;
}

