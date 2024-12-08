"use client";

import { redirect } from "next/navigation";

export default function AllGames({ allGames }: any) {
  return (
    <div>
      {allGames.map((game: any) => (
        <div key={game.id} className="flex" onClick={() => redirect(`/game/${game.id}`)}>
          <p className="mr-2">GameID: {game.id}</p>
          <p className="mr-2">Word Length : {game.wordLength} </p>
          <p>Date : {game.date} </p>
        </div>
      ))}
    </div>
  );
}
