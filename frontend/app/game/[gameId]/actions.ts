"use server"

import { getHeaders } from "@/app/connection"

export const fetchGame = async (gameId: number) => {
  const result_raw = await fetch(`http://localhost:5001/game/${gameId}`, {
    method: "GET",
    headers: await getHeaders(),
  })
  const result = await result_raw.json()
  return {
    id: result.game_id,
    wordLength: result.word_length,
    locked: result.locked,
    guesses: result.guesses.map(
      (guess: { word: string; hints: [number]; right_answer: boolean }) => ({
        word: guess.word,
        hints: guess.hints,
        right_answer: guess.right_answer,
      })
    ),
  }
}

export const sendGuess = async (prevState: GuessState, formData: FormData) => {
  const gameId = formData.get("gameId")
  const result = await fetch(`http://localhost:5001/game/${gameId}/guess`, {
    method: "POST",
    body: JSON.stringify({ guess: formData.get("guess") }),
    headers: await getHeaders(),
  })
  if (result.ok) {
    const new_guess = await result.json()
    return {
      ...prevState,
      error: null,
      guesses: [...prevState.guesses, new_guess],
    }
  } else {
    const response = await result.json()
    return {
      ...prevState,
      error: response.error,
      guesses: prevState.guesses,
    }
  }
}
