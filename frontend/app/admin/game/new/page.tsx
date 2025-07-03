import { createNewGame } from "./actions"

export default async function Game({ params }: any) {
  return (
    <form action={createNewGame}>
      <div className="flex flex-col gap-4">
        <div className="flex gap-4">
          <label htmlFor="word_length">Word Length:</label>
          <input type="number" name="word_length" className="text-black" />
        </div>
        <button type="submit">Create New Game</button>
      </div>
    </form>
  )
}
