'use server'

import { getHeaders } from "@/app/connection";

export const fetchCurrentGame = async () => {
    const result_raw = await fetch(`http://localhost:5001/game/current`, {
        method: "GET",
        headers: await getHeaders()
    },);
    const result = await result_raw.json()
    return {
        id: result.game_id,
        wordLength: result.word_length,
    };
}
