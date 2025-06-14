from backend.api.create_endpoints import create_endpoints
from backend.database.database import connect_database, init_database
from flask import Flask
from flask_cors import CORS
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
CORS(app)

connect_database()
init_database()


create_endpoints(app)
