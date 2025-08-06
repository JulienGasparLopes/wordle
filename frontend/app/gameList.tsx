"use client"

import { redirect } from "next/navigation"
import { userFormatDate } from "./helpers"
import { Trophy } from "lucide-react"

export default function AllGames({ allGames }: any) {
  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-2xl font-bold text-center">All games</h1>
      {allGames.map((game: any) => (
        <GameLine game={game} key={game.id} />
      ))}
    </div>
  )
}

const GameLine = ({ game }: any) => {
  const color = game.locked ? "gray-400" : "white"
  return (
    <div
      className={`border-solid border-${color} border rounded-md flex flex-col p-4 gap-4 text-${color}`}
    >
      <div
        className="flex gap-8 items-center cursor-pointer"
        onClick={() => redirect(`/game/${game.id}`)}
      >
        <GameState state={game.state} />
        <div>
          <div>Word Length : {game.wordLength}</div>
          <div>({userFormatDate(game.date)})</div>
        </div>
      </div>
      <button
        className="bg-orange-600 text-white rounded-md p-2 flex items-center justify-center gap-2 hover:bg-orange-700"
        onClick={() => redirect(`/game/${game.id}/leaderboard`)}
      >
        <Trophy size={16} />
        <span>Leaderboard</span>
      </button>
    </div>
  )
}

const GameState = ({ state }: { state: string }) => {
  const color =
    state === "NOT_STARTED"
      ? "bg-gray-500"
      : state === "IN_PROGRESS"
        ? "bg-yellow-500"
        : "bg-green-500"
  return <div className={`w-6 h-6 rounded-full ${color}`}></div>
}
