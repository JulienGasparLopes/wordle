import { cookies } from "next/headers"

export const getPseudo = async () => {
    const cookieStore = await cookies()
    return cookieStore.get('pseudo')?.value as string
}


export const getHeaders = async () => {
    return {
        'Content-Type': 'application/json',
        'Authorization': await getPseudo()
    }
}