import enum

from fastapi import HTTPException,Request
from starlette.responses import JSONResponse


class UserError(Exception):
    """Base exception class for all user-related errors"""
    pass


class UserExistsError(UserError):
    """Raised when attempting to create a user that already exists"""

    def __init__(self, email: str):
        super().__init__(f"User already exists")


class InvalidCredentialsError(UserError):
    """ Raised when invalid credentials are entered (email or password) """

    def __init__(self, message: str):
        super().__init__(f"{message}")


class DatabaseError(Exception):
    """Base exception class for all database-related errors"""

    def __init__(self, message: str):
        super().__init__(message)


class NotExistsError(Exception):
    """Base exception class for no entries found"""

    def __init__(self, message: str):
        super().__init__(message)


class ExistsError(Exception):
    """Base exception class for no entries found"""

    def __init__(self, message: str):
        super().__init__(message)


class InvalidOperationError(Exception):
    """Base exception class for invalid operations"""

    def __init__(self, message: str):
        super().__init__(message)

class InvalidRequestBody(Exception):
    """Base exception class for invalid request body"""

    def __init__(self,message: str):
        super().__init__(message)

class CustomHTTPException(HTTPException):
    def __init__(
            self,
            status_code: int,
            error_code:int,
            message: str,
    ) -> None:
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        super().__init__(status_code=status_code, detail=None)


async def custom_http_exception_handler(
    request: Request,
    exc: CustomHTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.error_code,
            "message": exc.message
        }
    )
