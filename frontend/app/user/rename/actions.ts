'use server'

import { getHeaders } from "@/app/connection";
import { redirect } from "next/navigation";

export const renameAction = async (formData: FormData) => {
    const pseudo = formData.get('pseudo') as string
    if (pseudo.length > 2) {
        const result = await fetch(`http://localhost:5001/user/rename`, {
            method: "POST",
            body: JSON.stringify({ pseudo }),
            headers: await getHeaders(),
        });
        if (result.ok) {
            redirect("/");
        }
    }
}
