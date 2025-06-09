from typing import Protocol
from backend.core.type_defs import Game, Guess, GuessHint, UserId
import datetime
from backend.database.database import DatabaseOld


class GameRepositoryPort(Protocol):
    def init_repository(self) -> None: ...

    def get_game(self, game_id: int) -> Game: ...

    def get_game_at_datetime(self, game_datetime: datetime.datetime) -> Game: ...

    def get_games(
        self,
        date_range: tuple[datetime.datetime, datetime.datetime] | None = None,
        pagination: tuple[int, int] | None = None,
    ) -> list[Game]: ...

    def add_game(self, word: str) -> Game: ...

    def get_guesses(
        self, *, game_id: int, user_id: UserId | None = None
    ) -> list[Guess]: ...

    def add_guess(self, guess: Guess) -> None: ...


class GameRepositoryOld:
    def __init__(self, database: DatabaseOld) -> None:
        self._database = database

    def init_repository(self) -> None:
        self._database.execute(
            """CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY,
                word TEXT UNIQUE,
                start_date DATETIME
            )
            """
        )
        self._database.execute(
            """CREATE TABLE IF NOT EXISTS guesses (
                id INTEGER PRIMARY KEY,
                game_id INTERGER,
                user_id INTERGER,
                word TEXT,
                guess_date DATETIME,
                clues TEXT,
                FOREIGN KEY(game_id) REFERENCES games(id),
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        )
        self._database.commit()

    def _db_values_to_game(self, raw_game: tuple) -> Game:
        return Game(
            id=raw_game[0],
            word=raw_game[1],
            start_date=datetime.datetime.strptime(raw_game[2], "%Y-%m-%d %H:%M:%S.%f"),
        )

    def _db_values_to_guess(self, raw_guess: tuple) -> Guess:
        return Guess(
            id=raw_guess[0],
            game_id=raw_guess[1],
            user_id=raw_guess[2],
            guess=raw_guess[3],
            guess_date=datetime.datetime.strptime(raw_guess[4], "%Y-%m-%d %H:%M:%S.%f"),
            clues=[GuessHint(int(clue)) for clue in raw_guess[5].split(",")],
        )

    def get_game(self, game_id: int) -> Game:
        raw_game = self._database.query_one("games", game_id)
        return self._db_values_to_game(raw_game)

    def get_game_at_datetime(self, game_datetime: datetime.datetime) -> Game:
        all_games_raw = self._database.query_all("games")
        all_games = [self._db_values_to_game(game) for game in all_games_raw]
        return max(
            [game for game in all_games if game.start_date <= game_datetime],
            key=lambda game: game.start_date,
        )

    def get_games(
        self,
        date_range: tuple[datetime.datetime, datetime.datetime] | None = None,
        pagination: tuple[int, int] | None = None,
    ) -> list[Game]:
        all_games_raw = self._database.query_all("games")
        all_games = [self._db_values_to_game(game) for game in all_games_raw]
        if date_range is not None:
            start_date, end_date = date_range
            return [
                game for game in all_games if start_date <= game.start_date <= end_date
            ]
        if pagination is not None:
            number_per_page, page_offset = pagination
            start = page_offset * number_per_page
            end = start + number_per_page
            return all_games[start:end]
        return all_games
        # TODO add frontend pagination
        # raise ValueError("Must provide date_range or pagination")

    def add_game(self, word: str) -> Game:
        self._database.execute(
            "INSERT INTO games (word, start_date) VALUES (?, ?)",
            (word, datetime.datetime.now()),
        )
        self._database.commit()
        game_id = self._database.get_last_row_id()
        return self.get_game(game_id)

    def get_guesses(
        self, *, game_id: int, user_id: UserId | None = None
    ) -> list[Guess]:
        if user_id is None:
            self._database.execute(
                "SELECT * FROM guesses WHERE game_id = ?",
                (game_id,),
            )
        else:
            self._database.execute(
                "SELECT * FROM guesses WHERE user_id = ? AND game_id = ?",
                (user_id, game_id),
            )
        raw_guesses = self._database.fetch_all()
        return [self._db_values_to_guess(guess) for guess in raw_guesses]

    def add_guess(self, guess: Guess) -> None:
        clues = ",".join([str(clue.value) for clue in guess.clues])
        self._database.execute(
            "INSERT INTO guesses (game_id, user_id, word, guess_date, clues) VALUES (?, ?, ?, ?, ?)",
            (guess.game_id, guess.user_id, guess.guess, guess.guess_date, clues),
        )
        self._database.commit()
