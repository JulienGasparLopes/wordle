import { redirect } from "next/navigation";
import { fetchGame, getPseudo, redirectToLogout } from "./actions";
import Guesses from "./guesses";

export default async function Game({ params }: any) {
  const gameId = (await params).gameId;
  const currentGame = await fetchGame(gameId);
  const pseudo = await getPseudo();

  return (
    <div className="h-full p-8 grid grid-rows-[70px_auto]">
      <div className="flex justify-between">
        <h2 className="text-4xl font-bold mb-8">
          {pseudo} - Game {gameId}
        </h2>
        <form>
          <button className="text-white" formAction={redirectToLogout}>
            Logout
          </button>
        </form>
      </div>
      <Guesses game={currentGame} />
    </div>
  );
}
