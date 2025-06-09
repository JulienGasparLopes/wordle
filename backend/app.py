from backend.api.create_endpoints import create_endpoints
from backend.core import make_game_repository, make_user_repository
from backend.database.database import (
    connect_database_old,
    connect_database,
    init_database,
)
from flask import Flask
from flask_cors import CORS
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
CORS(app)

connect_database_old()
connect_database()
init_database()

user_repository = make_user_repository()
user_repository.init_repository()

game_repository = make_game_repository()
game_repository.init_repository()

create_endpoints(app)


# For debuging purposes only
games = game_repository.get_games(pagination=(10, 0))
if not games:
    game_repository.add_game(word="world")
