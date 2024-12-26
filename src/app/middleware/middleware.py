import jwt
from fastapi import Request, HTTPException
from starlette import status
from starlette.middleware.base import RequestResponseEndpoint, BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.app.config.enumeration import Status
from src.app.model.responses import Response
from src.app.utils.context import set_user_to_context
from src.app.utils.utils import Utils
from src.app.config.messages import *
from src.app.config.custome_error_code import *

EXEMPT_ROUTES = ['/user/login', '/user/signup']
class AuthMiddleware(BaseHTTPMiddleware):
      async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(route) for route in EXEMPT_ROUTES):
            return await call_next(request)

        # Extract the Authorization header
        auth_token = request.headers.get('Authorization')
        if not auth_token or not auth_token.startswith('Bearer '):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=Response.response(MISSING_OR_INVALID_TOKEN, Status.FAIL.value, TOKEN_MISSING))

        token = auth_token.split(' ')[1]
        try:
            # Decode the JWT token
            decoded_token = Utils.decode_jwt_token(token)

            user_id = decoded_token.get("user_id")
            role = decoded_token.get("role")
            if not user_id or not role:
                raise HTTPException(
                status_code=401,
                detail=Response.response(INVALID_TOKEN, Status.FAIL.value, TOKEN_INVALID)
                )

            # Store user info in request state
            user_data = {
                "user_id": user_id,
                "role": role
            }
            set_user_to_context(request=request, user_data=user_data)


        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=401,
                content=Response.response(TOKEN_EXPIRE, Status.FAIL.value, TOKEN_EXPIRED)
            )
        except jwt.InvalidTokenError:
            return JSONResponse(
                status_code=401,
                content=Response.response(INVALID_TOKEN, Status.FAIL.value, TOKEN_INVALID)
            )

        # Continue to the next middleware or route handler
        return await call_next(request)