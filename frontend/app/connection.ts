import { auth0 } from "@/lib/auth0"
import { cookies } from "next/headers"

export const getPseudo = async () => {
    const cookieStore = await cookies()
    return cookieStore.get('pseudo')?.value as string
}


export const getHeaders = async () => {
    const sessionData = await auth0.getSession();

    return {
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + sessionData?.tokenSet?.accessToken,
    }
}