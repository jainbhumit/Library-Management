import functools
from flask import request, g
from src.app.utils.logger.logger import Logger


def api_logger(logger: Logger):
    def logger_wrapper(func):

        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            try:
                sanitized_body = logger._sanitize_body(request.get_json(silent=True) or {})
                user_id = getattr(g, 'user_id', 'Unknown')
                role = getattr(g, 'role', 'Unknown')

                logger.debug(
                    f"Entering {func.__name__}\n"
                    f"User Context:\n"
                    f"  - user_id: {user_id}\n"
                    f"  - role: {role}\n"
                    f"Request Context:\n"
                    f"  - method: {request.method}\n"
                    f"  - path: {request.path}\n"
                    f"  - client_ip: {request.remote_addr}\n"
                    f"  - headers: {dict(request.headers)}\n"
                    f"  - body: {sanitized_body}\n"
                    f"Function Context:\n"
                    f"  - handler: {type(args[0]).__name__ if args else 'Unknown'}\n"
                )

                result = func(*args, **kwargs)

                logger.info(f"{func.__name__} executed successfully.")
                return result
            except Exception as e:
                logger.error(
                    f"Error occurred in {func.__name__}: {str(e)}\n"
                    f"User Context:\n"
                    f"  - user_id: {user_id}\n"
                    f"  - role: {role}\n"
                    f"Request Context:\n"
                    f"  - method: {request.method}\n"
                    f"  - path: {request.path}\n"
                    f"  - client_ip: {request.remote_addr}\n"
                    f"  - body: {sanitized_body}"
                )
                raise
            finally:
                logger.debug(f"Exiting {func.__name__}")

        return wrapped_func

    return logger_wrapper
