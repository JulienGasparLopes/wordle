'use server'

import { getFormattedPseudo } from "@/app/actions";
import { redirect } from "next/navigation";

export const createNewGame = async (formData: FormData) => {
    const userPseudoId = await getFormattedPseudo()
    const word_length = formData.get("word_length");
    const result_raw = await fetch(`http://localhost:5001/game/new`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'Authorization': userPseudoId
        },
        body: JSON.stringify({
            "word_length": word_length
        })
    },);
    const result = await result_raw.json()
    console.log(result)
    redirect(`/`)
}
