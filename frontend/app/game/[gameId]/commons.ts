interface Guess {
    word: string;
    hints: number[];
    right_answer: boolean;
}

interface GuessState {
    error: string | null;
    guesses: Guess[];
}

interface Game {
    id: number;
    wordLength: number;
    guesses: Guess[];
}