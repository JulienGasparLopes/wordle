"use server"

import { getHeaders } from "@/app/connection"
import { redirect } from "next/navigation"

export const createNewGame = async (formData: FormData) => {
  const word_length = formData.get("word_length")
  const result_raw = await fetch(`http://localhost:5001/game/new`, {
    method: "POST",
    headers: await getHeaders(),
    body: JSON.stringify({
      word_length: word_length,
    }),
  })
  const result = await result_raw.json()
  redirect(`/`)
}
