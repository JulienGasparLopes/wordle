from backend.core.game_repository import (
    DeprecatedGameRepository,
    GameRepository,
    GameRepositoryPort,
)
from backend.core.user_repository import (
    DeprecatedUserRepository,
    UserRepository,
    UserRepositoryPort,
)
import backend.database.database as database


def make_user_repository() -> UserRepositoryPort:
    return UserRepository(database.database)


def make_deprecated_user_repository() -> UserRepositoryPort:
    return DeprecatedUserRepository(database.database)


def make_game_repository() -> GameRepositoryPort:
    return GameRepository(database.database)


def make_deprecated_game_repository() -> GameRepositoryPort:
    return DeprecatedGameRepository(database.database)
