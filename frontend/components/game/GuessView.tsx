"use client"

import { GuessState } from "@/app/game/[gameId]/commons"
import React, { useEffect } from "react"
import { LetterInput } from "./LetterInput"

export const GuessView = React.forwardRef(
  (
    {
      state,
      scrollRef,
      currentValue,
      setCurrentValue,
      answerFound,
    }: {
      state: GuessState
      scrollRef: any
      currentValue: string
      setCurrentValue: (value: string | ((prev: string) => string)) => void
      answerFound: boolean
    },
    ref
  ) => {
    let focusUsed = false
    const [isFocused, setIsFocused] = React.useState(false)

    const inputRef = React.useRef<HTMLInputElement>(null)

    React.useImperativeHandle(ref, () => ({
      focusInput: () => {
        if (inputRef.current) {
          inputRef.current.focus()
          const len = inputRef.current.value.length
          inputRef.current.setSelectionRange(len, len)
        }
      },
    }))

    useEffect(() => {
      inputRef.current?.focus()
    }, [])

    useEffect(() => {
      setCurrentValue("")
      scrollRef.current?.scrollTo(0, scrollRef.current?.scrollHeight)
    }, [state, scrollRef, setCurrentValue])

    return (
      <div className="flex flex-col justify-items-center">
        <input
          className="hidden"
          type="number"
          name="gameId"
          required={true}
          value={state.gameId}
          readOnly
        />
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
          onChange={(v) =>
            v.currentTarget.value.length <= state.wordLength &&
            setCurrentValue(v.currentTarget.value)
          }
          value={currentValue}
          disabled={answerFound}
        />
        <div
          className="flex gap-1"
          onClick={() => !answerFound && inputRef.current?.focus()}
        >
          {[...Array(state.wordLength)].map((_, index) => {
            const letter = currentValue?.[index]
            let focused = false
            if (isFocused && !focusUsed) {
              if (!letter || index === state.wordLength - 1) {
                focusUsed = true
                focused = true
              }
            }
            return (
              <LetterInput
                letter={currentValue?.[index]}
                focused={focused}
                key={index}
                disabled={answerFound}
              />
            )
          })}
        </div>
      </div>
    )
  }
)
GuessView.displayName = "GuessView"
