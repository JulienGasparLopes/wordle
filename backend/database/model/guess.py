import datetime
from backend.database.model.base_model import Base
from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped


class Guess(Base):
    __tablename__ = "guess"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    word: Mapped[str] = mapped_column(nullable=False)
    guess_date: Mapped[datetime.datetime] = mapped_column(
        nullable=False, default=datetime.datetime.now
    )
    hints: Mapped[str] = mapped_column(nullable=False)

    # TODO relationships

    def __repr__(self) -> str:
        return f"<Guess(id={self.id}, game_id={self.game_id}, user_id={self.user_id}, word='{self.word}')>"


class DeprecatedGuess(Base):
    __tablename__ = "guesses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    word: Mapped[str] = mapped_column(nullable=False)
    guess_date: Mapped[datetime.datetime] = mapped_column(
        nullable=False, default=datetime.datetime.now
    )
    clues: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"<Guess(id={self.id}, game_id={self.game_id}, user_id={self.user_id}, word='{self.word}')>"
