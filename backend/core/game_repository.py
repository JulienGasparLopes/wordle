from typing import Protocol
from backend.core.type_defs import Game, Guess, GuessHint
import datetime

repository: "GameRepositoryPort"


def connect_game_repository() -> None:
    global repository
    repository = GameRepository()


class GameRepositoryPort(Protocol):
    def get_game(
        self, game_id: int | None = None, game_datetime: datetime.datetime | None = None
    ) -> Game: ...

    def get_games(
        self,
        date_range: tuple[datetime.datetime, datetime.datetime] | None = None,
        pagination: tuple[int, int] | None = None,
    ) -> list[Game]: ...

    def add_game(self, word: str) -> Game: ...

    def get_guesses(self, user_id: int, game_id: int) -> list[Guess]: ...

    def add_guess(self, guess: Guess) -> None: ...


class GameRepository:
    def __init__(self):
        self._games = {
            1: Game(
                id=1, word="older", start_date=datetime.datetime(2021, 1, 1, hour=1)
            ),
            2: Game(
                id=2, word="world", start_date=datetime.datetime(2021, 3, 1, hour=1)
            ),
        }
        self._guesses = [*FAKE_GUESSES]

    def get_game(
        self, game_id: int | None = None, game_datetime: datetime.datetime | None = None
    ) -> Game:
        if game_id is not None:
            return self._games[game_id]
        if game_datetime is not None:
            return max(
                [
                    game
                    for game in self._games.values()
                    if game.start_date <= game_datetime
                ],
                key=lambda game: game.start_date,
            )
        raise ValueError("Must provide game_id or game_datetime")

    def get_games(
        self,
        date_range: tuple[datetime.datetime, datetime.datetime] | None = None,
        pagination: tuple[int, int] | None = None,
    ) -> list[Game]:
        if date_range is not None:
            start_date, end_date = date_range
            return [
                game
                for game in self._games.values()
                if start_date <= game.start_date <= end_date
            ]
        if pagination is not None:
            number_per_page, page_offset = pagination
            start = page_offset * number_per_page
            end = start + number_per_page
            return list(self._games.values())[start:end]
        raise ValueError("Must provide date_range or pagination")

    def add_game(self, word: str) -> Game:
        new_id = max(self._games.keys()) + 1
        new_game = Game(id=new_id, word=word, start_date=datetime.datetime.now())
        self._games[new_id] = new_game
        return new_game

    def get_guesses(self, user_id: int, game_id: int) -> list[Guess]:
        return [
            guess
            for guess in self._guesses
            if guess.user_id == user_id and guess.game_id == game_id
        ]

    def add_guess(self, guess: Guess) -> None:
        self._guesses.append(guess)


FAKE_GUESSES = [
    Guess(
        user_id=1,
        game_id=1,
        guess="xoder",
        clues=[
            GuessHint.INCORRECT,
            GuessHint.PRESENT,
            GuessHint.CORRECT,
            GuessHint.CORRECT,
            GuessHint.CORRECT,
        ],
        guess_date=datetime.datetime(2021, 1, 1, hour=3),
    ),
    Guess(
        user_id=1,
        game_id=1,
        guess="older",
        clues=[
            GuessHint.CORRECT,
            GuessHint.CORRECT,
            GuessHint.CORRECT,
            GuessHint.CORRECT,
            GuessHint.CORRECT,
        ],
        guess_date=datetime.datetime(2021, 1, 1, hour=4),
    ),
]
