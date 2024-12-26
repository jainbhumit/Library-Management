import logging
from contextvars import ContextVar
from logging.handlers import RotatingFileHandler
from threading import Lock
from typing import Optional
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

user_id_context: ContextVar[Optional[str]] = ContextVar('user_id', default='unknown')
user_role_context: ContextVar[Optional[str]] = ContextVar('user_role', default='unknown')

class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            user = getattr(request.state, 'user', {})
            user_id = user.get('user_id', 'unknown')
            role = user.get('role', 'unknown')
            # Set context variables
            user_id_context.set(user_id)
            user_role_context.set(role)

            response = await call_next(request)
            return response

        except Exception as e:
            Logger().error(f"Unhandled exception in middleware: {e}")
            raise

class Logger:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(Logger, cls).__new__(cls)
                cls._instance._initialize_logger()
            return cls._instance

    def _initialize_logger(self):
        self.logger = logging.getLogger("ThreadSafeLogger")
        self.logger.setLevel(logging.DEBUG)  # Set to the lowest level to capture all logs

        # Rotating File Handler (Thread-Safe)
        file_handler = RotatingFileHandler("app.log", maxBytes=5 * 1024 * 1024, backupCount=3)
        file_handler.setLevel(logging.DEBUG)

        # Custom Formatter with extra fields
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s - %(context)s"
        )
        file_handler.setFormatter(formatter)

        # Adding Handler
        self.logger.addHandler(file_handler)

    def sanitize_body(self, body):
        """
        Redacts sensitive information like passwords from the request body.
        """
        if not isinstance(body, dict):
            return body

        redacted_body = body.copy()
        sensitive_keys = {"password", "token", "secret"}  # Add other sensitive keys as needed
        for key in sensitive_keys:
            if key in redacted_body:
                redacted_body[key] = "***"  # Mask the sensitive value
        return redacted_body

    def _get_context(self):
        """Retrieve user_id and role from Flask's `g`."""
        user_id = user_id_context.get()
        role = user_role_context.get()
        return f"for user_id={user_id} | role={role}"

    # Convenience methods for logging
    def info(self, message: str):
        self.logger.info(message, extra={"context": self._get_context()})

    def error(self, message: str):
        self.logger.error(message, extra={"context": self._get_context()})

    def warning(self, message: str):
        self.logger.warning(message, extra={"context": self._get_context()})

    def debug(self, message: str):
        self.logger.debug(message, extra={"context": self._get_context()})
