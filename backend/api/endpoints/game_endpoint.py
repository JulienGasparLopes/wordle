from datetime import datetime
import json
from typing import Any

import backend.core.game_repository as game_repository
from backend.core.type_defs import Guess, GuessHint
from backend.core.word_service import WordService, WordServiceport
from flask import Blueprint, request
from pydantic import BaseModel

game_bp = Blueprint("template", __name__)

# TODO: use authed version to retrieve user info


class Game(BaseModel):
    game_id: int
    word_length: int
    start_date: datetime


class GameListReponse(BaseModel):
    games: list[Game]


@game_bp.route("/game", methods=["GET"])
def get_game_list() -> tuple[str, int]:
    games = game_repository.repository.get_games(pagination=(10, 0))

    response_object = GameListReponse(
        games=[
            Game(
                game_id=game.id,
                word_length=len(game.word),
                start_date=game.start_date,
            )
            for game in games
        ]
    )

    return response_object.model_dump_json(), 200


class GameGuessesResponse(BaseModel):
    word: str
    hints: list[int]
    guess_date: datetime


class GameResponse(BaseModel):
    game_id: int
    word_length: int
    start_date: datetime

    guesses: list[GameGuessesResponse]


@game_bp.route("/game/<game_id>/<user_id>", methods=["GET"])
def get_game(game_id: str, user_id: str) -> tuple[str, int]:
    game = game_repository.repository.get_game(game_id=int(game_id))

    user_guesses = game_repository.repository.get_guesses(
        user_id=int(user_id), game_id=game.id
    )

    response_object = GameResponse(
        game_id=game.id,
        word_length=len(game.word),
        start_date=game.start_date,
        guesses=[
            GameGuessesResponse(
                word=guess.guess,
                hints=[hint.value for hint in guess.clues],
                guess_date=guess.guess_date,
            )
            for guess in user_guesses
        ],
    )

    return response_object.model_dump_json(), 200


@game_bp.route("/game/current", methods=["GET"])
def get_current_game() -> tuple[str, int]:
    current_game = game_repository.repository.get_game(game_datetime=datetime.now())

    response_object = Game(
        game_id=current_game.id,
        word_length=len(current_game.word),
        start_date=current_game.start_date,
    )

    return response_object.model_dump_json(), 200


class AddGuessPayload(BaseModel):
    guess: str


class AddGuessResponse(BaseModel):
    word: str
    hints: list[int]
    right_answer: bool


@game_bp.route("/game/<game_id>/guess/<user_id>", methods=["POST"])
def post_guess(game_id: str, user_id: str) -> tuple[dict[str, Any], int]:
    word_service: WordServiceport = WordService()

    add_guest_payload = AddGuessPayload.model_validate(request.json)
    game = game_repository.repository.get_game(game_id=int(game_id))
    guesses = game_repository.repository.get_guesses(
        user_id=int(user_id), game_id=game.id
    )

    if any(guess.guess == game.word for guess in guesses):
        return {"error": "User already guessed this word"}, 400
    if any(guess.guess == add_guest_payload.guess for guess in guesses):
        return {"error": "User already tried this word"}, 400
    if len(add_guest_payload.guess) != len(game.word):
        return {"error": "Invalid word length"}, 400
    if not word_service.is_word_valid(add_guest_payload.guess):
        return {"error": "Invalid word"}, 400

    clues: list[GuessHint] = []
    for index, letter in enumerate(add_guest_payload.guess):
        if letter == game.word[index]:
            clues.append(GuessHint.CORRECT)
        elif letter in game.word:
            clues.append(GuessHint.PRESENT)
        else:
            clues.append(GuessHint.INCORRECT)

    user_guess = Guess(
        user_id=int(user_id),
        game_id=int(game_id),
        guess=add_guest_payload.guess,
        guess_date=datetime.now(),
        clues=clues,
    )

    game_repository.repository.add_guess(user_guess)

    response_object = AddGuessResponse(
        word=add_guest_payload.guess,
        hints=[hint.value for hint in clues],
        right_answer=add_guest_payload.guess == game.word,
    )

    return response_object.model_dump(), 200


class NewGamePayload(BaseModel):
    word_length: int


@game_bp.route("/game/new", methods=["POST"])
def post_new_game() -> tuple[dict[str, Any], int]:
    word_service: WordServiceport = WordService()
    payload = NewGamePayload.model_validate(request.json)
    new_word = word_service.get_random_word(payload.word_length)
    game_repository.repository.add_game(new_word)
    return {"word": new_word}, 200
