from dataclasses import dataclass
import datetime
from enum import Enum


@dataclass
class User:
    id: int
    username: str


@dataclass
class Game:
    id: int

    word: str
    start_date: datetime.datetime


class GuessHint(Enum):
    CORRECT = 0
    PRESENT = 1
    INCORRECT = 2


@dataclass
class Guess:
    user_id: int
    game_id: int
    guess: str
    guess_date: datetime.datetime
    clues: list[GuessHint]
