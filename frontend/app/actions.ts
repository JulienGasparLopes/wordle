'use server'

import { cookies } from "next/headers";
import { redirect } from "next/navigation";

export const redirectToAllGames = async () => {
    redirect("/")
}

export const redirectToLogout = async () => {
    redirect("/logout")
}

export const getPseudo = async () => {
    const cookieStore = await cookies()
    return cookieStore.get('pseudo')?.value as string
}


export const getFormattedPseudo = async () => {
    const rawPseudo = await getPseudo()
    return rawPseudo.toLowerCase().replace(" ", "_")
}

export const fetchAllGames = async () => {
    const userPseudoId = await getFormattedPseudo()

    const result_raw = await fetch(`https://127.0.0.1:5000/game`, {
        method: "GET",
        headers: {
            'Authorization': userPseudoId
        }
    },);
    const results = await result_raw.json()
    return results.games.map((result: { game_id: number, word_length: number, start_date: string }) => ({
        id: result.game_id,
        wordLength: result.word_length,
        date: result.start_date,
    }));
}
