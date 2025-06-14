from typing import Protocol
from backend.core.type_defs import Game, Guess, GuessHint, UserId
import datetime
from backend.database.database import Database
from backend.database.model import Game as GameModel, Guess as GuessModel
from backend.database.model.guess import DeprecatedGuess as DeprecatedGuessModel
from backend.database.model.game import DeprecatedGame as DeprecatedGameModel


class GameRepositoryPort(Protocol):
    def get_game(self, game_id: int) -> Game: ...

    def get_game_at_datetime(self, game_datetime: datetime.datetime) -> Game: ...

    def get_games(
        self,
        date_range: tuple[datetime.datetime, datetime.datetime] | None = None,
        pagination: tuple[int, int] | None = None,
    ) -> list[Game]: ...

    def add_game(self, word: str, start_date: datetime.datetime) -> Game: ...

    def get_guesses(
        self, *, game_id: int, user_id: UserId | None = None
    ) -> list[Guess]: ...

    def add_guess(self, guess: Guess) -> None: ...

    def lock_game(self, game_id: int) -> None: ...

    def unlock_game(self, game_id: int) -> None: ...


class GameRepository(GameRepositoryPort):
    def __init__(self, database: Database) -> None:
        self._database = database

    def get_game(self, game_id: int) -> Game:
        with self._database.get_session() as session:
            raw_game = session.get(GameModel, game_id)

        return Game(
            id=raw_game.id,
            word=raw_game.word,
            start_date=raw_game.start_date,
            locked=raw_game.locked,
        )

    def get_game_at_datetime(self, game_datetime: datetime.datetime) -> Game:
        all_games = self.get_games()
        return max(
            [game for game in all_games if game.start_date <= game_datetime],
            key=lambda game: game.start_date,
        )

    def get_games(
        self,
        date_range: tuple[datetime.datetime, datetime.datetime] | None = None,
        pagination: tuple[int, int] | None = None,
    ) -> list[Game]:
        with self._database.get_session() as session:
            raw_games = session.query(GameModel).all()

        return [
            Game(
                id=game.id,
                word=game.word,
                start_date=game.start_date,
                locked=game.locked,
            )
            for game in raw_games
        ]

    def add_game(self, word: str, start_date: datetime.datetime) -> Game:
        with self._database.get_session() as session:
            new_game = GameModel(
                word=word,
                start_date=start_date,
                locked=False,
            )
            session.add(new_game)
            session.commit()
            session.refresh(new_game)

        return Game(
            id=new_game.id,
            word=new_game.word,
            start_date=new_game.start_date,
            locked=new_game.locked,
        )

    def get_guesses(
        self, *, game_id: int, user_id: UserId | None = None
    ) -> list[Guess]:
        with self._database.get_session() as session:
            query = session.query(GuessModel).filter(GuessModel.game_id == game_id)
            if user_id is not None:
                query = query.filter(GuessModel.user_id == user_id)

            raw_guesses = query.all()

        return [
            Guess(
                id=guess.id,
                user_id=guess.user_id,
                game_id=guess.game_id,
                guess=guess.word,
                guess_date=guess.guess_date,
                hints=[GuessHint(int(clue)) for clue in guess.hints.split(",")],
            )
            for guess in raw_guesses
        ]

    def add_guess(self, guess: Guess) -> None:
        with self._database.get_session() as session:
            new_guess = GuessModel(
                game_id=guess.game_id,
                user_id=guess.user_id,
                word=guess.guess,
                guess_date=guess.guess_date,
                hints=",".join([str(clue.value) for clue in guess.hints]),
            )
            session.add(new_guess)
            session.commit()

    def lock_game(self, game_id: int) -> None:
        with self._database.get_session() as session:
            game = session.get(GameModel, game_id)
            if game:
                game.locked = True
                session.commit()

    def unlock_game(self, game_id: int) -> None:
        with self._database.get_session() as session:
            game = session.get(GameModel, game_id)
            if game:
                game.locked = False
                session.commit()


class DeprecatedGameRepository(GameRepositoryPort):
    def __init__(self, database: Database) -> None:
        self._database = database

    def get_games(
        self,
        date_range: tuple[datetime.datetime, datetime.datetime] | None = None,
        pagination: tuple[int, int] | None = None,
    ) -> list[Game]:
        with self._database.get_session() as session:
            raw_games = session.query(DeprecatedGameModel).all()

        return [
            Game(id=game.id, word=game.word, start_date=game.start_date, locked=False)
            for game in raw_games
        ]

    def get_guesses(
        self, *, game_id: int, user_id: UserId | None = None
    ) -> list[Guess]:
        with self._database.get_session() as session:
            query = session.query(DeprecatedGuessModel).filter(
                DeprecatedGuessModel.game_id == game_id
            )
            if user_id is not None:
                query = query.filter(DeprecatedGuessModel.user_id == user_id)

            raw_guesses = query.all()

        return [
            Guess(
                id=guess.id,
                user_id=guess.user_id,
                game_id=guess.game_id,
                guess=guess.word,
                guess_date=guess.guess_date,
                hints=[GuessHint(int(clue)) for clue in guess.clues.split(",")],
            )
            for guess in raw_guesses
        ]

    def get_game(self, game_id: int) -> Game: ...

    def get_game_at_datetime(self, game_datetime: datetime.datetime) -> Game: ...

    def add_game(self, word: str, start_date: datetime.datetime) -> Game: ...

    def add_guess(self, guess: Guess) -> None: ...

    def lock_game(self, game_id: int) -> None: ...

    def unlock_game(self, game_id: int) -> None: ...
