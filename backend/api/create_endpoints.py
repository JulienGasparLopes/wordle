from flask import Flask
from backend.api.endpoints.game_endpoint import game_bp
from backend.api.endpoints.user_endpoints import user_bp


def create_endpoints(app: Flask) -> None:
    app.register_blueprint(game_bp)
    app.register_blueprint(user_bp)
