from dataclasses import dataclass
import datetime
from enum import Enum

UserId = int
GameId = int
GuessId = int


@dataclass
class User:
    id: UserId
    username: str


@dataclass
class Game:
    id: GameId

    word: str
    start_date: datetime.datetime


class GuessHint(Enum):
    CORRECT = 0
    PRESENT = 1
    INCORRECT = 2


@dataclass
class Guess:
    id: GuessId
    user_id: UserId
    game_id: GameId
    guess: str
    guess_date: datetime.datetime
    clues: list[GuessHint]
