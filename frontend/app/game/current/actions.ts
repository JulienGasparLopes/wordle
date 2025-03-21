'use server'

import { getFormattedPseudo } from "@/app/actions";

export const fetchCurrentGame = async () => {
    const userPseudoId = await getFormattedPseudo()
    const result_raw = await fetch(`https://wordle-cbuv.onrender.com/game/current`, {
        method: "GET",
        headers: {
            'Authorization': userPseudoId
        }
    },);
    const result = await result_raw.json()
    return {
        id: result.game_id,
        wordLength: result.word_length,
    };
}
