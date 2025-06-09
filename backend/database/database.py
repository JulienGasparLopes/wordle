import sqlite3
from typing import Any

from backend.database.model.base_model import Base
from sqlalchemy import create_engine

database: "DatabaseOld"


def connect_database_old() -> None:
    global database
    database = DatabaseOld()


class DatabaseOld:
    def __init__(self):
        self._connection = sqlite3.connect("database.db", check_same_thread=False)
        self._cursor = self._connection.cursor()

    def commit(self):
        self._connection.commit()

    def execute(self, query: str, params: tuple[Any, ...] = ()) -> Any:
        self._cursor.execute(query, params)

    def fetch_one(self) -> Any:
        return self._cursor.fetchone()

    def fetch_all(self) -> Any:
        return self._cursor.fetchall()

    def get_last_row_id(self) -> int:
        return self._cursor.lastrowid

    def query_one(self, table: str, id: int) -> Any:
        self.execute(f"SELECT * FROM {table} WHERE id = ?", (id,))
        return self.fetch_one()

    def query_all(self, table: str) -> Any:
        self.execute(f"SELECT * FROM {table}")
        return self.fetch_all()


database: "Database"


def connect_database() -> None:
    global database
    database = Database()


def init_database() -> None:
    Base.metadata.create_all(bind=database._engine)


class Database:
    def __init__(self):
        self._engine = create_engine(
            "sqlite:///database.db", connect_args={"check_same_thread": False}
        )

    def get_session(self):
        return self._engine.begin()
