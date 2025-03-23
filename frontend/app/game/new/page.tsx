import { createNewGame } from "./actions";

export default async function Game({ params }: any) {
  return (
    <div>
      <form>
        <input type="number" name="word_length" className="text-black" />
        <button formAction={createNewGame}>Create New Game</button>
      </form>
    </div>
  );
}
