from typing import Protocol

from core.database import Database
from core.type_defs import User, UserId


class UnfoundUserError(Exception): ...


class UserRepositoryPort(Protocol):
    def init_repository(self) -> None: ...

    def get_user(self, user_id: UserId) -> User: ...

    def get_user_by_pseudo(self, pseudo: str) -> User: ...

    def create_user(self, pseudo: str) -> User: ...


class UserRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    def init_repository(self) -> None:
        self._database.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                pseudo TEXT UNIQUE
            )
            """
        )
        self._database.commit()

    def get_user(self, user_id: UserId) -> User:
        raw_user = self._database.query_one("users", user_id)
        return User(id=raw_user[0], username=raw_user[1])

    def get_user_by_pseudo(self, pseudo: str) -> User:
        try:
            self._database.execute(f"SELECT * FROM users WHERE pseudo = ?", (pseudo,))
            raw_user = self._database.fetch_one()
            return User(id=raw_user[0], username=raw_user[1])
        except Exception as e:
            raise UnfoundUserError()

    def create_user(self, pseudo: str) -> User:
        self._database.execute("INSERT INTO users (pseudo) VALUES (?)", (pseudo,))
        self._database.commit()
        return self.get_user(self._database.get_last_row_id())
