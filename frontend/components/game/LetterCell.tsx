"use client"

import {
  COLOR_ABSENT,
  COLOR_CORRECT,
  COLOR_NEUTRAL,
  COLOR_PRESENT,
} from "@/app/game/[gameId]/commons"

export const hintToColor = (hint: number) => {
  switch (hint) {
    case 0:
      return COLOR_CORRECT
    case 1:
      return COLOR_PRESENT
    case 2:
      return COLOR_ABSENT
    default:
      return COLOR_NEUTRAL
  }
}

export const LetterCell = ({
  letter,
  color,
  onClick,
}: {
  letter: string
  color: string
  onClick?: () => void
}) => {
  return (
    <div
      onClick={onClick}
      className={`rounded-sm w-10 h-10 ${color} leading-5 justify-items-center justify-center flex items-center ${
        onClick ? "cursor-pointer" : ""
      }`}
    >
      <p className="text-xl">{letter}</p>
    </div>
  )
}
