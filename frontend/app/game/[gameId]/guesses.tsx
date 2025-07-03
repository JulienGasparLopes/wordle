"use client"

import { GuessView } from "@/components/game/GuessView"
import { LetterCell, hintToColor } from "@/components/game/LetterCell"
import { VirtualKeyboard } from "@/components/game/VirtualKeyboard"
import React, { useEffect } from "react"
import { sendGuess } from "./actions"
import { Game, Guess, GuessState } from "./commons"

export default function Guesses({ game }: { game: Game }) {
  const [state, formAction] = React.useActionState<GuessState, any>(sendGuess, {
    error: null,
    gameId: game.id,
    wordLength: game.wordLength,
    locked: game.locked,
    guesses: game.guesses,
  })

  const [currentValue, setCurrentValue] = React.useState("")
  const guessSelectorRef = React.useRef<{ focusInput: () => void }>(null)

  const answerFound = React.useMemo(
    () =>
      state.guesses.length > 0 &&
      state.guesses.some((guess: Guess) => guess.right_answer),
    [state.guesses]
  )

  const letterToHint = React.useMemo(() => {
    const result: { [letter: string]: number } = {}
    state.guesses.forEach((guess: Guess) => {
      guess.word.split("").forEach((letter: string, index: number) => {
        const letterLower = letter.toLowerCase()
        if (
          result[letterLower] === undefined ||
          result[letterLower] > guess.hints[index]
        ) {
          result[letterLower] = guess.hints[index]
        }
      })
    })
    return result
  }, [state.guesses])

  const scrollRef = React.useRef<HTMLDivElement>(null)

  const handleLetterClick = (letter: string) => {
    if (currentValue.length < state.wordLength && !answerFound) {
      setCurrentValue(currentValue + letter)
    }
    setTimeout(() => guessSelectorRef.current?.focusInput(), 0)
  }

  const handleDelete = () => {
    setCurrentValue((cv) => cv.slice(0, -1))
    setTimeout(() => guessSelectorRef.current?.focusInput(), 0)
  }

  const handleClear = () => {
    setCurrentValue("")
    setTimeout(() => guessSelectorRef.current?.focusInput(), 0)
  }

  return (
    <div className="mx-auto w-1/2 h-9/10 grid grid-rows-[auto_auto_auto] gap-8 justify-items-center justify-center">
      <div
        ref={scrollRef}
        className="overflow-y-scroll"
        style={{ scrollbarColor: "white black" }}
      >
        {state.guesses.map((guess: Guess, index: number) => (
          <div className="flex gap-1 mb-1" key={index}>
            {guess.word.split("").map((letter: string, letterIndex: number) => {
              const color = hintToColor(guess.hints[letterIndex])
              return (
                <LetterCell letter={letter} color={color} key={letterIndex} />
              )
            })}
          </div>
        ))}
      </div>
      {!!state.locked ? (
        <div className="text-gray-400 w-48 text-center">Game is locked</div>
      ) : (
        <form action={formAction} className="contents">
          <GuessView
            ref={guessSelectorRef}
            state={state}
            scrollRef={scrollRef}
            currentValue={currentValue}
            setCurrentValue={setCurrentValue}
            answerFound={answerFound}
          />
          <VirtualKeyboard
            letterToHint={letterToHint}
            onLetterClick={handleLetterClick}
            onDelete={handleDelete}
            onClear={handleClear}
            answerFound={answerFound}
          />
          {state.error && <div className="text-red-500">{state.error}</div>}
        </form>
      )}
    </div>
  )
}
