from backend.core import make_user_repository
from flask import Flask, request, g
from backend.api.endpoints.game_endpoint import game_bp


def create_endpoints(app: Flask) -> None:
    app.register_blueprint(game_bp)

    @app.before_request
    def before_request():
        user_pseudo = request.headers.get("Authorization")
        if not user_pseudo:
            return "Unauthorized", 401

        user_pseudo = user_pseudo.lower().replace(" ", "_")

        # Wrong pattern that implies calling the database before each request
        user_repository = make_user_repository()
        try:
            user = user_repository.get_user_by_pseudo(user_pseudo)
        except Exception as e:
            user = user_repository.create_user(user_pseudo)

        g.user_id = user.id
