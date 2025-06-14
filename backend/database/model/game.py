import datetime
from backend.database.model.base_model import Base
from sqlalchemy.orm import mapped_column, Mapped


class Game(Base):
    __tablename__ = "game"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(nullable=False)
    start_date: Mapped[datetime.datetime] = mapped_column(
        nullable=False, default=datetime.datetime.now
    )
    locked: Mapped[bool] = mapped_column(nullable=False, default=False)

    def __repr__(self) -> str:
        return f"<Game(id={self.id}, word='{self.word}', start_date={self.start_date})>"


class DeprecatedGame(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(nullable=False)
    start_date: Mapped[datetime.datetime] = mapped_column(
        nullable=False, default=datetime.datetime.now
    )

    def __repr__(self) -> str:
        return f"<Game(id={self.id}, word='{self.word}', start_date={self.start_date})>"
