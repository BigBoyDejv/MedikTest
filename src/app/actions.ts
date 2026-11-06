"use server";

import { revalidatePath } from "next/cache";
import { createClient } from "@/utils/supabase/server";

export async function recordQuestionProgressAction(
  questionId: string,
  isCorrect: boolean
) {
  const supabase = createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return { error: "Pre uloženie výsledku do histórie sa prosím prihláste." };
  }

  const { error } = await supabase.from("user_progress").insert({
    user_id: user.id,
    question_id: questionId,
    is_correct: isCorrect,
  });

  if (error) {
    return { error: error.message };
  }

  revalidatePath("/");
  return { success: true };
}

