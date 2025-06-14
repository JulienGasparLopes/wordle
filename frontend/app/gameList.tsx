"use client";

import { redirect } from "next/navigation";
import { userFormatDate } from "./helpers";

export default function AllGames({ allGames }: any) {
  return (
    <div className="flex flex-col gap-4">
      {allGames.map((game: any) => (
        <GameLine game={game} key={game.id} />
      ))}
    </div>
  );
}

const GameLine = ({ game }: any) => {
  const color = game.locked ? "gray-400" : "white";
  return (
    <div className="flex gap-8">
      <div
        className={`border-solid border-${color} border rounded-md flex p-2 px-4 gap-8 text-${color}`}
        onClick={() => redirect(`/game/${game.id}`)}
      >
        <GameState state={game.state} />
        <div>Word Length : {game.wordLength}</div>
        <div>({userFormatDate(game.date)})</div>
      </div>
      <div className="self-center" onClick={() => redirect(`/game/${game.id}/leaderboard`)}>
        Leaderboard
      </div>
    </div>
  );
};

const GameState = ({ state }: { state: string }) => {
  const color = state === "NOT_STARTED" ? "bg-gray-500" : state === "IN_PROGRESS" ? "bg-yellow-500" : "bg-green-500";
  return <div className={`w-6 h-6 rounded-xl ${color}`}></div>;
};
