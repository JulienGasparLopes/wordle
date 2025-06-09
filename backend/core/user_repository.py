from typing import Protocol

from backend.database.database import DatabaseOld
from backend.core.type_defs import User, UserId


class UnfoundUserError(Exception): ...


class UserRepositoryPort(Protocol):
    def init_repository(self) -> None: ...

    def get_user(self, user_id: UserId) -> User: ...

    def get_user_by_formatted_pseudo(self, formatted_pseudo: str) -> User: ...

    def create_user(self, pseudo: str) -> User: ...

    def rename_user(self, user_id: UserId, new_pseudo: str) -> User: ...


class UserRepositoryOld(UserRepositoryPort):
    def __init__(self, database: DatabaseOld) -> None:
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

    def get_user(self, user_id: UserId) -> User:
        raw_user = self._database.query_one("users", user_id)
        return User(id=raw_user[0], pseudo=raw_user[1], formatted_pseudo=raw_user[2])

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

    def create_user(self, pseudo: str) -> User:
        formatted_pseudo = pseudo.lower().replace(" ", "_")
        self._database.execute(
            "INSERT INTO users (pseudo, formatted_pseudo) VALUES (?, ?)",
            (pseudo, formatted_pseudo),
        )
        self._database.commit()
        return self.get_user(self._database.get_last_row_id())

    def rename_user(self, user_id: UserId, new_pseudo: str) -> User:
        self._database.execute(
            "UPDATE users SET pseudo = ? WHERE id = ?",
            (new_pseudo, user_id),
        )
        self._database.commit()
        return self.get_user(user_id)
