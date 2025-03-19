'use server'

import { cookies } from "next/headers";
import { redirect } from "next/navigation";


export const redirectToLogout = async () => {
    redirect("/logout")
}

export const getPseudo = async () => {
    const cookieStore = await cookies()
    return cookieStore.get('pseudo')?.value as string
}

export const fetchAllGames = async () => {
    const result_raw = await fetch(`http://127.0.0.1:5000/game`, {
        method: "GET",
    },);
    const results = await result_raw.json()
    return results.games.map((result: any) => ({
        id: result.game_id,
        wordLength: result.word_length,
        date: result.start_date,
    }));
}
