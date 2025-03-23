import { getLeaderboard } from "./actions";

export default async function Game({ params }: any) {
  const gameId = (await params).gameId;
  const userResults = await getLeaderboard(gameId);

  return (
    <>
      {userResults.map((result: any) => (
        <div key={result.id}>
          <div>{result.pseudo}</div>
          <div>{result.score}</div>
        </div>
      ))}
    </>
  );
}
