from backend.core.game_repository import GameRepository, GameRepositoryPort
from backend.core.user_repository import UserRepository, UserRepositoryPort
import backend.core.database as database


def make_user_repository() -> UserRepositoryPort:
    return UserRepository(database.database)


def make_game_repository() -> GameRepositoryPort:
    return GameRepository(database.database)
