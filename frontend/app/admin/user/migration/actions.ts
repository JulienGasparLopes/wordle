'use server'

import { getHeaders } from "@/app/connection";

export const getUserInformation = async () => {
    const result_raw = await fetch(`http://localhost:5001/admin/user/migration`, {
        method: "GET",
        headers: await getHeaders()
    },);
    return await result_raw.json()
}
