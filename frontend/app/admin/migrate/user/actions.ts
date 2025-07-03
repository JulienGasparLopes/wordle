"use server"

import { getHeaders } from "@/app/connection"
import { redirect } from "next/navigation"

export const getUserInformation = async () => {
  const result_raw = await fetch(`http://localhost:5001/admin/migrate/user`, {
    method: "GET",
    headers: await getHeaders(),
  })
  return await result_raw.json()
}

export const migrateUser = async (formData: FormData) => {
  const new_user_id = parseInt(formData.get("new_user_id") as string)
  const old_user_id = parseInt(formData.get("old_user_id") as string)

  if (new_user_id && old_user_id) {
    const response = await fetch(`http://localhost:5001/admin/migrate/user`, {
      method: "POST",
      body: JSON.stringify({ new_user_id, old_user_id }),
      headers: await getHeaders(),
    })
    if (response.ok) {
      redirect("/")
    } else {
      redirect("/admin")
    }
  }
}
