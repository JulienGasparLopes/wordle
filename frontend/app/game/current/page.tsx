import { redirect } from "next/navigation"
import { fetchCurrentGame } from "./actions"

export default async function Game({ params }: any) {
  const gameId = (await params).gameId
  const currentGame = await fetchCurrentGame()

  redirect(`/game/${currentGame.id}`)

  return <div></div>
}
