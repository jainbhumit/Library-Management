import jwt
from flask import request, jsonify, g

from src.app.config.enumeration import Status
from src.app.model.responses import Response
from src.app.utils.utils import Utils
from src.app.config.messages import *
from src.app.config.custome_error_code import *


def auth_middleware():
    if request.path in ['/user/login','/user/signup']:
        return None

    auth_token = request.headers.get('Authorization')
    if not auth_token or not auth_token.startswith('Bearer '):
        return Response.response(MISSING_OR_INVALID_TOKEN,Status.FAIL.value,TOKEN_MISSING),401

    token = auth_token.split(' ')[1]
    try:
        decoded_token = Utils.decode_jwt_token(token)

        user_id = decoded_token.get("user_id")
        role = decoded_token.get("role")

        if not user_id or not role:
            return Response.response(INVALID_TOKEN,Status.FAIL.value,TOKEN_INVALID),401

        g.user_id = user_id
        g.role = role

    except jwt.ExpiredSignatureError:
        return Response.response(TOKEN_EXPIRE,Status.FAIL.value,TOKEN_EXPIRED),401
    except jwt.InvalidTokenError:
        return Response.response(INVALID_TOKEN,Status.FAIL.value,TOKEN_INVALID),401