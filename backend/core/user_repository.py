from typing import Protocol, override

from backend.core.database import Database
from backend.core.type_defs import User, UserId


class UnfoundUserError(Exception): ...


class UserRepositoryPort(Protocol):
    def init_repository(self) -> None: ...

    def get_user(self, user_id: UserId) -> User: ...

    def get_user_by_formatted_pseudo(self, formatted_pseudo: str) -> User: ...

    def create_user(self, pseudo: str) -> User: ...


class UserRepository(UserRepositoryPort):
    def __init__(self, database: Database) -> None:
        self._database = database

    def init_repository(self) -> None:
        self._database.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                pseudo TEXT UNIQUE,
                formatted_pseudo TEXT UNIQUE
            )
            """
        )
        self._database.commit()

    @override
    def get_user(self, user_id: UserId) -> User:
        raw_user = self._database.query_one("users", user_id)
        return User(id=raw_user[0], pseudo=raw_user[1], formatted_pseudo=raw_user[2])

    @override
    def get_user_by_formatted_pseudo(self, formatted_pseudo: str) -> User:
        try:
            self._database.execute(
                f"SELECT * FROM users WHERE formatted_pseudo = ?", (formatted_pseudo,)
            )
            raw_user = self._database.fetch_one()
            return User(
                id=raw_user[0], pseudo=raw_user[1], formatted_pseudo=raw_user[2]
            )
        except Exception as e:
            raise UnfoundUserError()

    @override
    def create_user(self, pseudo: str) -> User:
        formatted_pseudo = pseudo.lower().replace(" ", "_")
        self._database.execute(
            "INSERT INTO users (pseudo, formatted_pseudo) VALUES (?, ?)",
            (pseudo, formatted_pseudo),
        )
        self._database.commit()
        return self.get_user(self._database.get_last_row_id())
