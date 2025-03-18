from typing import Protocol

from backend.core.type_defs import User, UserId

repository: "UserRepositoryPort"


def connect_user_repository() -> None:
    global repository
    repository = UserRepository()


class UserRepositoryPort(Protocol):
    def get_user(self, user_id: UserId) -> User: ...


class UserRepository:
    def __init__(self):
        self._users = {
            1: User(id="pinzen", username="Pinzen"),
            2: User(id="bobby", username="Bobby"),
        }

    def get_user(self, user_id: UserId) -> User:
        return self._users[user_id]
