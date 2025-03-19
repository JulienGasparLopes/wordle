'use server'

import { getPseudo } from "@/app/actions";


const getFormattedPseudo = async () => {
    const rawPseudo = await getPseudo()
    return rawPseudo.toLowerCase().replace(" ", "_")
}

export const fetchGame = async (gameId: number) => {
    const userPseudoId = await getFormattedPseudo()
    const result_raw = await fetch(`http://127.0.0.1:5000/game/${gameId}/${userPseudoId}`, {
        method: "GET",
    },);
    const result = await result_raw.json()
    return {
        id: result.game_id,
        wordLength: result.word_length,
        guesses: result.guesses.map((guess: any) => ({
            word: guess.word,
            hints: guess.hints,
            right_answer: guess.right_answer,
        })),
    };
}


export const sendGuess = async (prevState: GuessState, formData: FormData) => {
    const userPseudoId = await getFormattedPseudo()
    const gameId = formData.get('gameId')
    const result = await fetch(`http://127.0.0.1:5000/game/${gameId}/guess/${userPseudoId}`, {
        method: "POST",
        body: JSON.stringify({ guess: formData.get('guess') }),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    if (result.ok) {
        const new_guess = await result.json()
        return {
            error: null,
            guesses: [...prevState.guesses, new_guess]
        }
    }
    else {
        const response = await result.json()
        return {
            error: response.error,
            guesses: prevState.guesses
        }
    }
}