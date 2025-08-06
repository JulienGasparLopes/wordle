from functools import wraps
import json
from urllib.request import urlopen
from backend.core import make_user_repository
from flask import request, g
import os
from jose import jwt

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
API_AUDIENCE = os.environ.get("AUTH0_AUDIENCE")
ALGORITHMS = ["RS256"]


# Fetch JWKS (public keys)
def get_jwks():
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    return json.loads(jsonurl.read())


def get_token_auth_header():
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise Exception("Authorization header is expected")
    parts = auth.split()
    if parts[0].lower() != "bearer":
        raise Exception("Authorization header must start with Bearer")
    elif len(parts) == 1:
        raise Exception("Token not found")
    elif len(parts) > 2:
        raise Exception("Authorization header must be Bearer token")
    return parts[1]


def verify_decode_jwt(token):
    jwks = get_jwks()
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if rsa_key:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/",
        )
        return payload
    raise Exception("Unable to find appropriate key")


def require_auth(require_admin_role: bool = False):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
                connection_id = payload.get("sub", "")

                # Wrong pattern that implies calling the database before each request
                user_repository = make_user_repository()
                try:
                    user = user_repository.get_user_by_connection_id(connection_id)
                except Exception as e:
                    user = user_repository.create_user(connection_id)

                g.user_id = user.id
            except Exception as e:
                raise Exception("Unauthorized") from e
            return f(*args, **kwargs)

        return decorated

    return wrapper
