from typing import Protocol


from backend.database.database import Database
from backend.core.type_defs import User, UserId
from backend.database.model import User as UserModel
from backend.database.model.guess import DeprecatedGuess
from backend.database.model.user import DeprecatedUser as DeprecatedUserModel


class UnfoundUserError(Exception): ...


class UserRepositoryPort(Protocol):
    def get_user(self, user_id: UserId) -> User: ...

    def get_users(self) -> list[User]: ...

    def get_user_by_connection_id(self, connection_id: str) -> User: ...

    def create_user(self, pseudo: str) -> User: ...

    def rename_user(self, user_id: UserId, new_pseudo: str) -> User: ...

    def delete_user(self, user_id: UserId) -> None: ...


class UserRepository(UserRepositoryPort):
    def __init__(self, database: Database) -> None:
        self._database = database

    def get_user(self, user_id: UserId) -> User:
        with self._database.get_session() as session:
            raw_user = session.get(UserModel, user_id)
        return User(
            id=raw_user.id,
            pseudo=raw_user.pseudo,
            is_admin=raw_user.is_admin,
        )

    def get_users(self) -> list[User]:
        with self._database.get_session() as session:
            raw_users = session.query(UserModel).all()
        return [
            User(id=user.id, pseudo=user.pseudo, is_admin=user.is_admin)
            for user in raw_users
        ]

    def get_user_by_connection_id(self, connection_id: str) -> User:
        with self._database.get_session() as session:
            raw_user = (
                session.query(UserModel)
                .filter(UserModel.connection_id == connection_id)
                .one()
            )
        return User(id=raw_user.id, pseudo=raw_user.pseudo, is_admin=raw_user.is_admin)

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

    def delete_user(self, user_id: UserId) -> None:
        raise NotImplementedError(
            "User deletion is not implemented in the new repository."
        )


class DeprecatedUserRepository(UserRepositoryPort):
    def __init__(self, database: Database) -> None:
        self._database = database

    def get_user(self, user_id: UserId) -> User: ...

    def get_users(self) -> list[User]:
        with self._database.get_session() as session:
            raw_users = session.query(DeprecatedUserModel).all()
        return [
            User(id=user.id, pseudo=user.pseudo, is_admin=False) for user in raw_users
        ]

    def get_user_by_connection_id(self, connection_id: str) -> User: ...

    def create_user(self, pseudo: str) -> User: ...

    def rename_user(self, user_id: UserId, new_pseudo: str) -> User: ...

    def delete_user(self, user_id: UserId) -> None:
        with self._database.get_session() as session:
            user = session.get(DeprecatedUserModel, user_id)
            if not user:
                raise UnfoundUserError(f"User with ID {user_id} not found.")
            session.query(DeprecatedGuess).filter(
                DeprecatedGuess.user_id == user_id
            ).delete()
            session.delete(user)
            session.commit()
