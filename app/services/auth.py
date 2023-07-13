import datetime
import re
from functools import wraps

import jwt
from flask import abort, request, g

import config
from app.services.app_exceptions import AuthenticationException
from app.services.token_helper import decode_token


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'Authorization' not in request.headers or len(request.headers.get('Authorization')) < 10:
            raise AuthenticationException()

        try:
            token = request.headers.get('Authorization', None)[7:]
            g.user_token = decode_token(token)
        except Exception:
            raise AuthenticationException()

        return f(*args, **kws)

    return decorated_function
