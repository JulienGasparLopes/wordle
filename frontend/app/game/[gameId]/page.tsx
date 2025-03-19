import { fetchGame } from "./actions";
import Guesses from "./guesses";

export default async function Game({ params }: any) {
  const gameId = (await params).gameId;
  const currentGame = await fetchGame(gameId);

  return <Guesses game={currentGame} />;
}
