'use server'

import { getHeaders } from "@/app/connection";


export const migrateGames = async () => {
    const result = await fetch(`http://localhost:5001/admin/migrate/game`, {
        method: "POST",
        headers: await getHeaders(),
    });
    return await result.json()
}