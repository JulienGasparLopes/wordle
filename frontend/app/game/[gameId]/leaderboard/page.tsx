import { userFormatDate } from "@/app/helpers"
import { getLeaderboard } from "./actions"

export default async function Game({ params }: any) {
  const gameId = (await params).gameId
  const userResults = await getLeaderboard(gameId)

  return (
    <>
      {userResults.length === 0 && <div>No results yet</div>}
      {userResults.map((result: any, index: number) => (
        <PlayerResult key={index} result={result} />
      ))}
    </>
  )
}

const PlayerResult = ({ result }: any) => {
  // First ugly hardcode <3
  const hasRainboxText =
    result.user_id === 8 && Date.now() > new Date("2025-06-26").getTime()
  const rainbowTextClass = hasRainboxText ? "rainbow_text_animated" : ""

  return (
    <div className={`flex flex-column gap-4 ${rainbowTextClass}`}>
      <div>{result.user_pseudo}</div>
      <div>|</div>
      <div>Guess counts: {result.guess_count}</div>
      <div>|</div>
      <div>{userFormatDate(result.win_date)}</div>
    </div>
  )
}
