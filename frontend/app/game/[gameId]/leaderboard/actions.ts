'use server'

import { getHeaders } from "@/app/connection";


export const getLeaderboard = async (gameId: number) => {
    const result_raw = await fetch(`http://localhost:5001/game/${gameId}/leaderboard`, {
        method: "GET",
        headers: await getHeaders()
    },);
    const result = await result_raw.json()

    return result["leaderboard"].sort((a: { index: number }, b: { index: number }) => a.index - b.index);
}

