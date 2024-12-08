'use server'

export const fetchCurrentGame = async () => {
    const result_raw = await fetch(`http://127.0.0.1:5000/game/current`, {
        method: "GET",
    },);
    const result = await result_raw.json()
    return {
        id: result.game_id,
        wordLength: result.word_length,
    };
}
