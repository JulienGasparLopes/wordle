import { fetchAllGames } from "./actions";
import AllGames from "./gameList";

export default async function Home() {
  const allGames = await fetchAllGames();

  return <AllGames allGames={allGames} />;
}
