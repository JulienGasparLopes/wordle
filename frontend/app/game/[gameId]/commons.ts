export const COLOR_NEUTRAL = 'bg-gray-400'
export const COLOR_CORRECT = 'bg-green-600'
export const COLOR_PRESENT = 'bg-orange-500'
export const COLOR_ABSENT = 'bg-red-600'

export interface Guess {
  word: string
  hints: number[]
  right_answer: boolean
}

export interface GuessState {
  error: string | null
  gameId: number
  wordLength: number
  locked: boolean
  guesses: Guess[]
}

export interface Game {
  id: number
  wordLength: number
  guesses: Guess[]
  locked: boolean
}
