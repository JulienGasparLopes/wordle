from os import environ as env

from backend.api.create_endpoints import create_endpoints
from backend.core.game_repository import connect_game_repository
from backend.core.user_repository import connect_user_repository
from flask import Flask
from flask_cors import CORS
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
CORS(app)

connect_game_repository()
connect_user_repository()

# oauth = OAuth(app)
# oauth.register(
#     "auth0",
#     client_id=env.get("AUTH0_CLIENT_ID"),
#     client_secret=env.get("AUTH0_CLIENT_SECRET"),
#     client_kwargs={
#         "scope": "openid profile email",
#     },
#     server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
# )


create_endpoints(app)
