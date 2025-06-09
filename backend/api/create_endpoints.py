from backend.core import make_user_repository
from flask import Flask, request, g
from backend.api.endpoints.game_endpoint import game_bp


def create_endpoints(app: Flask) -> None:
    app.register_blueprint(game_bp)
