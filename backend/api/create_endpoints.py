from flask import Flask
from backend.api.endpoints.game_endpoint import game_bp


def create_endpoints(app: Flask) -> None:
    app.register_blueprint(game_bp)
