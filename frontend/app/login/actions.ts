'use server'

import { cookies } from "next/headers";
import { redirect } from "next/navigation";

export const loginAction = async (formData: FormData) => {
    const pseudo = formData.get('pseudo') as string
    const cookieStore = await cookies();
    if (pseudo.length > 2) {
        cookieStore.set("pseudo", pseudo);
        cookieStore.set("login_date", new Date().toISOString());
        redirect("/game/current");
    }
}
