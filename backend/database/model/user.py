from backend.database.model.base_model import Base
from sqlalchemy.orm import mapped_column, Mapped


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    connection_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    pseudo: Mapped[str] = mapped_column(nullable=False)

    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)

    def __repr__(self) -> str:
        return f"<UserModel(id={self.id}, pseudo='{self.pseudo}')>"


class DeprecatedUser(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pseudo: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"<DeprecatedUserModel(id={self.id}, pseudo='{self.pseudo}')>"
