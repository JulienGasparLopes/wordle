'use server'

export const fetchGame = async (gameId: number) => {
    const result_raw = await fetch(`http://127.0.0.1:5000/game/${gameId}/1`, {
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
    const gameId = formData.get('gameId')
    const result = await fetch(`http://127.0.0.1:5000/game/${gameId}/guess/1`, {
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