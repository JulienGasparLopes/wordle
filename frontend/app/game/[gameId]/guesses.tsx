"use client";

import React, { useEffect } from "react";
import { sendGuess } from "./actions";

export default function Guesses({ game }: { game: Game }) {
  const [state, formAction] = React.useActionState<GuessState, any>(sendGuess, {
    error: null,
    guesses: game.guesses,
  });
  const [currentValue, setCurrentValue] = React.useState("");
  const [isFocused, setIsFocused] = React.useState(true);

  const inputRef = React.useRef<HTMLInputElement>(null);

  useEffect(() => {
    setCurrentValue("");
  }, [state]);

  let focusUsed = false;

  return (
    <div className="mx-auto w-1/2 flex-col justify-items-center justify-center">
      {state.guesses.map((guess: Guess, index: number) => (
        <div className="flex gap-1 mb-1" key={index}>
          {guess.word.split("").map((letter: string, letter_index: number) => {
            const color =
              guess.hints[letter_index] === 0
                ? "bg-green-600"
                : guess.hints[letter_index] === 1
                ? "bg-orange-500"
                : "bg-red-600";
            return (
              <div
                className={`rounded-sm w-5 h-5 ${color} leading-5 justify-items-center justify-center`}
                key={letter_index}
              >
                <p>{letter}</p>
              </div>
            );
          })}
        </div>
      ))}
      <form className="flex flex-col justify-items-center">
        <input className="hidden" type="number" name="gameId" required={true} value={game.id} readOnly />
        <input
          ref={inputRef}
          className="w-0 h-0"
          autoComplete="off"
          type="text"
          name="guess"
          required={true}
          autoFocus
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          onChange={(v) => v.currentTarget.value.length <= game.wordLength && setCurrentValue(v.currentTarget.value)}
          value={currentValue}
        />
        <div className="flex gap-1" onClick={() => inputRef.current?.focus()}>
          {[...Array(game.wordLength)].map((_, index) => {
            const letter = currentValue?.[index];
            let focused = false;
            if (isFocused && !focusUsed) {
              if (!letter || index === game.wordLength - 1) {
                focusUsed = true;
                focused = true;
              }
            }
            const borderClass = focused ? "border-cyan-500 border-2" : "border-white border-2";
            return (
              <div
                className={`text-black rounded-sm w-5 h-5 bg-white leading-4 justify-items-center justify-center ${borderClass}`}
                key={index}
              >
                <p>{currentValue?.[index]}</p>
              </div>
            );
          })}
        </div>
        <button formAction={formAction}>Upload</button>
      </form>
      {state.error && <div>{state.error}</div>}
    </div>
  );
}
