import datetime
import jwt
import config
from flask import request


def generate_token(user_groups, username):
    jwt_auth_token = jwt.encode(
        {
            "user_groups": user_groups,
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=int(config.AUTH_EXP_TIME)),
            "ip": get_user_ip()

        },
        config.JWT_SECRET_KEY, 'HS256'
    )
    return jwt_auth_token


def decode_token(token):
    decoded_token = jwt.decode(token, config.JWT_SECRET_KEY, 'HS256')
    return decoded_token


def get_user_ip():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr

    return ip
