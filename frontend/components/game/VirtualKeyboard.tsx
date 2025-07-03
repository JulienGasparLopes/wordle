"use client"

import { Eraser, Send, Trash2 } from "lucide-react"
import { LetterCell, hintToColor } from "./LetterCell"

const ALL_LETTERS = "abcdefghijklmnopqrstuvwxyz"

export const VirtualKeyboard = ({
  letterToHint,
  onLetterClick,
  onDelete,
  onClear,
  answerFound,
}: {
  letterToHint: { [letter: string]: number }
  onLetterClick: (letter: string) => void
  onDelete: () => void
  onClear: () => void
  answerFound: boolean
}) => {
  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-wrap gap-1 mt-4 justify-center select-none">
        {ALL_LETTERS.split("").map((letter) => (
          <LetterCell
            key={letter}
            letter={letter}
            color={hintToColor(letterToHint[letter])}
            onClick={() => onLetterClick(letter)}
          ></LetterCell>
        ))}
      </div>
      <div className="flex justify-center gap-2">
        <button
          type="button"
          onClick={onDelete}
          disabled={answerFound}
          className="px-4 py-2 rounded bg-gray-600 text-white hover:bg-gray-700 disabled:bg-gray-800 disabled:text-gray-500 flex items-center gap-2"
        >
          <Eraser size={16} />
          Delete
        </button>
        <button
          type="button"
          onClick={onClear}
          disabled={answerFound}
          className="px-4 py-2 rounded bg-red-600 text-white hover:bg-red-700 disabled:bg-gray-800 disabled:text-gray-500 flex items-center gap-2"
        >
          <Trash2 size={16} />
          Clear
        </button>
        <button
          type="submit"
          disabled={answerFound}
          className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 disabled:bg-gray-800 disabled:text-gray-500 flex items-center gap-2"
        >
          <Send size={16} />
          Try
        </button>
      </div>
    </div>
  )
}
