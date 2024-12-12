import functools

from src.app.utils.logger.logger import Logger


def api_logger(logger: Logger):
    def logger_wrapper(func):

        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            try:
                logger.debug(f"Entering {func.__name__} with args: {args}, kwargs: {kwargs}")
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} executed successfully.")
                return result
            except Exception as e:
                logger.error(f"Error occurred in {func.__name__}: {str(e)}")
                raise
            finally:
                logger.debug(f"Exiting {func.__name__}")

        return wrapped_func

    return logger_wrapper