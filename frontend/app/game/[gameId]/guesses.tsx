"use client";

import React, { useEffect } from "react";
import { sendGuess } from "./actions";

const ALL_LETTERS = "abcdefghijklmnopqrstuvwxyz";

const COLOR_NEUTRAL = "bg-gray-400";
const COLOR_CORRECT = "bg-green-600";
const COLOR_PRESENT = "bg-orange-500";
const COLOR_ABSENT = "bg-red-600";

export default function Guesses({ game }: { game: Game }) {
  const [state, formAction] = React.useActionState<GuessState, any>(sendGuess, {
    error: null,
    gameId: game.id,
    wordLength: game.wordLength,
    locked: game.locked,
    guesses: game.guesses,
  });

  const letterToHint = React.useMemo(() => {
    const result: { [letter: string]: number } = {};
    state.guesses.forEach((guess: Guess) => {
      guess.word.split("").forEach((letter: string, index: number) => {
        const letter_lower = letter.toLowerCase();
        if (result[letter_lower] === undefined || result[letter_lower] > guess.hints[index]) {
          result[letter_lower] = guess.hints[index];
        }
      });
    });
    return result;
  }, [state.guesses]);

  const scrollRef = React.useRef<HTMLDivElement>(null);

  return (
    <div className="mx-auto w-1/2 h-9/10 grid grid-rows-[auto_auto_auto] gap-8 justify-items-center justify-center">
      <div ref={scrollRef} className="overflow-y-scroll" style={{ scrollbarColor: "white black" }}>
        {state.guesses.map((guess: Guess, index: number) => (
          <div className="flex gap-1 mb-1" key={index}>
            {guess.word.split("").map((letter: string, letter_index: number) => {
              const color = hintToColor(guess.hints[letter_index]);
              return <LetterCell letter={letter} color={color} key={letter_index} />;
            })}
          </div>
        ))}
      </div>
      {!!state.locked ? (
        <div className="text-gray-400 w-48 text-center">Game is locked</div>
      ) : (
        <>
          <GuessSelector state={state} formAction={formAction} scrollRef={scrollRef} />
          <LetterStateIndicator letterToHint={letterToHint} />
        </>
      )}
    </div>
  );
}

const GuessSelector = ({ state, formAction, scrollRef }: { state: GuessState; formAction: any; scrollRef: any }) => {
  let focusUsed = false;
  const answer_found = state.guesses.length > 0 && state.guesses.some((guess: Guess) => guess.right_answer);

  const [currentValue, setCurrentValue] = React.useState("");
  const [isFocused, setIsFocused] = React.useState(true);

  const inputRef = React.useRef<HTMLInputElement>(null);

  useEffect(() => {
    setCurrentValue("");
    scrollRef.current?.scrollTo(0, scrollRef.current?.scrollHeight);
  }, [state]);

  return (
    <form className="flex flex-col justify-items-center">
      <input className="hidden" type="number" name="gameId" required={true} value={state.gameId} readOnly />
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
        onChange={(v) => v.currentTarget.value.length <= state.wordLength && setCurrentValue(v.currentTarget.value)}
        value={currentValue}
      />
      <div className="flex gap-1" onClick={() => !answer_found && inputRef.current?.focus()}>
        {[...Array(state.wordLength)].map((_, index) => {
          const letter = currentValue?.[index];
          let focused = false;
          if (isFocused && !focusUsed) {
            if (!letter || index === state.wordLength - 1) {
              focusUsed = true;
              focused = true;
            }
          }
          return <LetterInput letter={currentValue?.[index]} focused={focused} key={index} disabled={answer_found} />;
        })}
      </div>
      <button disabled={answer_found} formAction={formAction} className={answer_found ? "text-gray-400" : "text-white"}>
        Send Answer
      </button>
      {state.error && <div>{state.error}</div>}
    </form>
  );
};

const LetterStateIndicator = ({ letterToHint }: { letterToHint: { [letter: string]: number } }) => {
  return (
    <div className="flex flex-wrap gap-1 mt-4 justify-center">
      {ALL_LETTERS.split("").map((letter) => (
        <LetterCell key={letter} letter={letter} color={hintToColor(letterToHint[letter])}></LetterCell>
      ))}
    </div>
  );
};

const LetterCell = ({ letter, color }: { letter: string; color: string }) => {
  return (
    <div className={`rounded-sm w-10 h-10 ${color} leading-5 justify-items-center justify-center flex items-center`}>
      <p className="text-xl">{letter}</p>
    </div>
  );
};

const LetterInput = ({ letter, focused, disabled }: { letter: string; focused: boolean; disabled: boolean }) => {
  const borderClass = disabled ? "border-gray-400" : focused ? "border-cyan-500 border-2" : "border-white border-2";
  const color = disabled ? "bg-gray-400" : "bg-white";
  return (
    <div
      className={`text-black rounded-sm w-10 h-10 ${color} leading-4 justify-items-center justify-center ${borderClass} flex items-center`}
    >
      <p className="text-xl">{letter}</p>
    </div>
  );
};

const hintToColor = (hint: number) => {
  switch (hint) {
    case 0:
      return COLOR_CORRECT;
    case 1:
      return COLOR_PRESENT;
    case 2:
      return COLOR_ABSENT;
    default:
      return COLOR_NEUTRAL;
  }
};
