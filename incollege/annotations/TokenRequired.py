from functools import wraps

import jwt
from flask import request

from incollege.exceptions.AuthException import AuthException
from incollege.services import AuthService


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'token' in request.headers:
            token = request.headers['token']
        if not token:
            raise AuthException("Authentication token missing.")
        token_data = None
        try:
            token_data = AuthService.decode_token(token)
        except jwt.ExpiredSignatureError:
            raise AuthException("Session expired.")
        except jwt.InvalidTokenError:
            raise AuthException("Authentication failed.")
        return f(token_data, *args, **kwargs)
    return decorated
