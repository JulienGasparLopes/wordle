from typing import Protocol

from backend.core.type_defs import User

repository: "UserRepositoryPort"


def connect_user_repository() -> None:
    global repository
    repository = UserRepository()


class UserRepositoryPort(Protocol):
    def get_user(self, user_id: int) -> User: ...


class UserRepository:
    def __init__(self):
        self._users = {
            1: User(id=1, username="test_user1"),
            2: User(id=2, username="test_user2"),
        }

    def get_user(self, user_id: int) -> User:
        return self._users[user_id]
