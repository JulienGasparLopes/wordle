from backend.core.game_repository import GameRepositoryOld, GameRepositoryPort
from backend.core.user_repository import UserRepositoryOld, UserRepositoryPort
import backend.database.database as database


def make_user_repository() -> UserRepositoryPort:
    return UserRepositoryOld(database.database)


def make_game_repository() -> GameRepositoryPort:
    return GameRepositoryOld(database.database)
