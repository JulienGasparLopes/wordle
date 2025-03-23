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
  return (
    <div className="flex gap-8">
      <div
        className="border-solid border-white border rounded-md flex p-2 gap-8"
        onClick={() => redirect(`/game/${game.id}`)}
      >
        <div>Word Length : {game.wordLength}</div>
        <div>({userFormatDate(game.date)})</div>
      </div>
      <div className="self-center" onClick={() => redirect(`/game/${game.id}/leaderboard`)}>
        Leaderboard
      </div>
    </div>
  );
};
