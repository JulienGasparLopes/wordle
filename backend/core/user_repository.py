from typing import Protocol


from backend.database.database import Database
from backend.core.type_defs import User, UserId
from backend.database.model import User as UserModel


class UnfoundUserError(Exception): ...


class UserRepositoryPort(Protocol):
    def get_user(self, user_id: UserId) -> User: ...

    def get_user_by_connection_id(self, connection_id: str) -> User: ...

    def create_user(self, pseudo: str) -> User: ...

    def rename_user(self, user_id: UserId, new_pseudo: str) -> User: ...


class UserRepository(UserRepositoryPort):
    def __init__(self, database: Database) -> None:
        self._database = database

    def get_user(self, user_id: UserId) -> User:
        with self._database.get_session() as session:
            raw_user = session.get(UserModel, user_id)
        return User(
            id=raw_user.id, pseudo=raw_user.pseudo, formatted_pseudo=raw_user.pseudo
        )

    def get_user_by_connection_id(self, connection_id: str) -> User:
        with self._database.get_session() as session:
            raw_user = (
                session.query(UserModel)
                .filter(UserModel.connection_id == connection_id)
                .one()
            )
        return User(
            id=raw_user.id, pseudo=raw_user.pseudo, formatted_pseudo=raw_user.pseudo
        )

    def create_user(self, connection_id: str) -> User:
        with self._database.get_session() as session:
            new_user = UserModel(
                pseudo="New Player",
                connection_id=connection_id,
            )
            session.add(new_user)
            session.commit()
        return self.get_user(new_user.id)

    def rename_user(self, user_id: UserId, new_pseudo: str) -> User:
        with self._database.get_session() as session:
            user = session.get(UserModel, user_id)
            user.pseudo = new_pseudo
            session.commit()
        return self.get_user(user_id)
