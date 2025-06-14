from datetime import datetime
from typing import Any, Literal

from backend.core import (
    make_deprecated_game_repository,
    make_game_repository,
    make_user_repository,
)
from backend.core.type_defs import Guess, GuessHint
from backend.core.word_service import WordService, WordServiceport
from flask import Blueprint, request, g
from pydantic import BaseModel
from backend.api.validator import require_auth

game_bp = Blueprint("game_bp", __name__)


class Game(BaseModel):
    game_id: int
    word_length: int
    start_date: datetime
    locked: bool


class GameInfo(Game):
    state: Literal["NOT_STARTED", "IN_PROGRESS", "FINISHED"]


class GameListReponse(BaseModel):
    games: list[GameInfo]


@game_bp.route("/game", methods=["GET"])
@require_auth()
def get_game_list() -> tuple[str, int]:
    user_id: str = g.user_id

    game_repository = make_game_repository()
    games = game_repository.get_games()  # TODO add pagination=(10, 0)

    formatted_games: list[GameInfo] = []
    for game in games:
        user_guesses = game_repository.get_guesses(game_id=game.id, user_id=user_id)
        if not user_guesses:
            state = "NOT_STARTED"
        elif any(
            guess.hints == [GuessHint.CORRECT] * len(guess.guess)
            for guess in user_guesses
        ):
            state = "FINISHED"
        else:
            state = "IN_PROGRESS"

        formatted_games.append(
            GameInfo(
                game_id=game.id,
                word_length=len(game.word),
                start_date=game.start_date,
                state=state,
                locked=game.locked,
            )
        )

    response_object = GameListReponse(games=formatted_games)

    return response_object.model_dump_json(), 200


class GameGuessesResponse(BaseModel):
    word: str
    hints: list[int]
    right_answer: bool
    guess_date: datetime


class GameResponse(BaseModel):
    game_id: int
    word_length: int
    start_date: datetime
    locked: bool

    guesses: list[GameGuessesResponse]


@game_bp.route("/game/<game_id>", methods=["GET"])
@require_auth()
def get_game(game_id: str) -> tuple[str, int]:
    user_id: str = g.user_id

    game_repository = make_game_repository()
    game = game_repository.get_game(game_id=int(game_id))

    user_guesses = game_repository.get_guesses(game_id=game.id, user_id=user_id)

    response_object = GameResponse(
        game_id=game.id,
        word_length=len(game.word),
        start_date=game.start_date,
        locked=game.locked,
        guesses=[
            GameGuessesResponse(
                word=guess.guess,
                hints=[hint.value for hint in guess.hints],
                right_answer=guess.guess == game.word,
                guess_date=guess.guess_date.isoformat(),
            )
            for guess in user_guesses
        ],
    )

    return response_object.model_dump_json(), 200


@game_bp.route("/game/current", methods=["GET"])
@require_auth()
def get_current_game() -> tuple[str, int]:
    game_repository = make_game_repository()
    current_game = game_repository.get_game_at_datetime(game_datetime=datetime.now())

    response_object = Game(
        game_id=current_game.id,
        word_length=len(current_game.word),
        start_date=current_game.start_date.isoformat(),
        locked=current_game.locked,
    )

    return response_object.model_dump_json(), 200


class AddGuessPayload(BaseModel):
    guess: str


class AddGuessResponse(BaseModel):
    word: str
    hints: list[int]
    right_answer: bool


@game_bp.route("/game/<game_id>/guess", methods=["POST"])
@require_auth()
def post_guess(game_id: str) -> tuple[dict[str, Any], int]:
    user_id: str = g.user_id

    word_service: WordServiceport = WordService()
    game_repository = make_game_repository()

    game = game_repository.get_game(game_id=int(game_id))

    if game.locked:
        return {"error": "Game is locked"}, 403

    add_guest_payload = AddGuessPayload.model_validate(request.json)
    word_guess = add_guest_payload.guess.lower()
    guesses = game_repository.get_guesses(game_id=game.id, user_id=user_id)

    if any(guess.guess == game.word for guess in guesses):
        return {"error": "User already guessed this word"}, 400
    if any(guess.guess == word_guess for guess in guesses):
        return {"error": "User already tried this word"}, 400
    if len(word_guess) != len(game.word):
        return {"error": "Invalid word length"}, 400
    if not word_service.is_word_valid(word_guess):
        return {"error": "Invalid word"}, 400

    hints: list[GuessHint] = []
    for index, letter in enumerate(word_guess):
        if letter == game.word[index]:
            hints.append(GuessHint.CORRECT)
        elif letter in game.word:
            hints.append(GuessHint.PRESENT)
        else:
            hints.append(GuessHint.INCORRECT)

    user_guess = Guess(
        id=-1,
        user_id=user_id,
        game_id=int(game_id),
        guess=add_guest_payload.guess,
        guess_date=datetime.now(),
        hints=hints,
    )

    game_repository.add_guess(user_guess)

    response_object = AddGuessResponse(
        word=add_guest_payload.guess,
        hints=[hint.value for hint in hints],
        right_answer=add_guest_payload.guess == game.word,
    )

    return response_object.model_dump(), 200


class NewGamePayload(BaseModel):
    word_length: int


@game_bp.route("/game/new", methods=["POST"])
@require_auth(require_admin_role=True)
def post_new_game() -> tuple[dict[str, Any], int]:
    word_service: WordServiceport = WordService()
    game_repository = make_game_repository()

    payload = NewGamePayload.model_validate(request.json)
    while True:
        new_word = word_service.get_random_word(payload.word_length)
        if len(new_word) == len({letter for letter in new_word}):
            break

    game_repository.add_game(new_word, start_date=datetime.now())
    return {"word": new_word}, 200


@game_bp.route("/game/<game_id>/leaderboard", methods=["GET"])
@require_auth()
def get_game_leaderboard(game_id: str) -> tuple[dict[str, Any], int]:
    game_repository = make_game_repository()
    user_repository = make_user_repository()

    guesses = game_repository.get_guesses(game_id=int(game_id))
    guesses_by_user_id: dict[int, list[Guess]] = {}
    user_who_guessed = set()
    for guess in guesses:
        if guess.hints == [GuessHint.CORRECT] * len(guess.guess):
            user_who_guessed.add(guess.user_id)

        if guess.user_id not in guesses_by_user_id:
            guesses_by_user_id[guess.user_id] = []
        guesses_by_user_id[guess.user_id].append(guess)

    leaderboard = [
        {
            "user_pseudo": user_repository.get_user(user_id).pseudo,
            "guess_count": len(user_guesses),
            "win_date": user_guesses[0].guess_date.isoformat(),
        }
        for user_id, user_guesses in guesses_by_user_id.items()
        if user_id in user_who_guessed
    ]
    sorted_leaderboard = sorted(
        leaderboard, key=lambda x: (x["guess_count"], x["win_date"])
    )
    for index, entry in enumerate(sorted_leaderboard):
        entry["index"] = index

    return {"leaderboard": sorted_leaderboard}, 200


# temporary endpoints
@game_bp.route("/admin/migrate/game", methods=["POST"])
@require_auth(require_admin_role=True)
def migrate_games() -> tuple[dict[str, Any], int]:
    game_repository = make_game_repository()
    deprecated_game_repository = make_deprecated_game_repository()

    old_game_by_word = {
        game.word: game for game in deprecated_game_repository.get_games()
    }
    new_game_by_word = {game.word: game for game in game_repository.get_games()}

    migrated_games: list[str] = []
    for word, old_game in old_game_by_word.items():
        if word not in new_game_by_word:
            created_game = game_repository.add_game(
                word, start_date=old_game.start_date
            )
            game_repository.lock_game(created_game.id)
            migrated_games.append(word)

    return {
        "migrated_games": migrated_games,
        "count": len(migrated_games),
    }, 200
