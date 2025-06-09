from backend.database.model.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


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

    def get_session(self) -> Session:
        return Session(self._engine)
