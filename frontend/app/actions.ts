'use server'

import { redirect } from "next/navigation";
import { getHeaders, getPseudo } from "./connection";

export const redirectToAllGames = async () => {
    redirect("/")
}

export const redirectToLogout = async () => {
    redirect("/logout")
}

export const fetchAllGames = async () => {
    const userPseudo = await getPseudo()

    const result_raw = await fetch(`http://localhost:5001/game`, {
        method: "GET",
        headers: await getHeaders()
    },);
    const results_raw = await result_raw.json()
    const results = results_raw.games.map((result: { game_id: number, word_length: number, start_date: string }) => ({
        id: result.game_id,
        wordLength: result.word_length,
        date: result.start_date,
    }));
    return results.sort((a: { date: string; }, b: { date: string; }) => new Date(b.date).getTime() - new Date(a.date).getTime())
}
