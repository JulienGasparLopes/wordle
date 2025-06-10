from typing import Any
from backend.api.validator import require_auth
from backend.core import make_deprecated_user_repository, make_user_repository
from flask import Blueprint, g, request
from pydantic import BaseModel


user_bp = Blueprint("user_bp", __name__)


class RenamePayload(BaseModel):
    pseudo: str


@user_bp.route("/user/rename", methods=["POST"])
@require_auth()
def post_rename() -> tuple[dict[str, Any], int]:
    user_id: str = g.user_id
    payload: RenamePayload = RenamePayload.model_validate(request.json)

    user_repository = make_user_repository()

    user_repository.rename_user(user_id, payload.pseudo)

    return {"status": "ok"}, 200


class UserInfoPayload(BaseModel):
    pseudo: str
    is_admin: bool


@user_bp.route("/user/current", methods=["GET"])
@require_auth()
def get_current_user_info() -> tuple[dict[str, Any], int]:
    user_id: str = g.user_id

    user_repository = make_user_repository()
    user = user_repository.get_user(user_id)

    user_info = UserInfoPayload(
        pseudo=user.pseudo,
        is_admin=user.is_admin,
    )

    return user_info.model_dump(), 200


# temporary endpoints


class UserInfoMigrationPayload(BaseModel):
    id: int
    pseudo: str


class UserMigrationAvailableUsersPayload(BaseModel):
    new_users: list[UserInfoMigrationPayload]
    old_users: list[UserInfoMigrationPayload]


@user_bp.route("/admin/user/migration", methods=["GET"])
@require_auth(require_admin_role=True)
def get_user_migration_info() -> tuple[dict[str, Any], int]:
    user_repository = make_user_repository()
    deprecated_user_repository = make_deprecated_user_repository()
    users = user_repository.get_users()
    old_users = deprecated_user_repository.get_users()

    user_info_list = [
        UserInfoMigrationPayload(id=user.id, pseudo=user.pseudo).model_dump()
        for user in users
    ]
    old_user_info_list = [
        UserInfoMigrationPayload(id=user.id, pseudo=user.pseudo).model_dump()
        for user in old_users
    ]

    payload = UserMigrationAvailableUsersPayload(
        new_users=user_info_list,
        old_users=old_user_info_list,
    )

    return payload.model_dump(), 200
