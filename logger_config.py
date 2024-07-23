import logging
from functools import lru_cache
from logging import Logger, StreamHandler, FileHandler, Handler, Formatter
from typing import Type


@lru_cache(maxsize=2 ** 12)
def get_logger(name: str | None = None) -> Logger:
    """
    Get a logger instance with the given name. This function caches logger instances to avoid reconfiguring them.

    :param name: The name of the logger. Defaults to None.
    :return: A logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Set the logging level
        logger.setLevel(logging.INFO)

        # Create and add handlers
        stream_handler = setup_handler(StreamHandler)
        file_handler = setup_handler(FileHandler, filename='app.log')
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

    logger.propagate = False
    return logger


def setup_handler(handler_cls: Type[Handler], level: int = logging.INFO, **kwargs) -> Handler:
    """
    General function to set up a logging handler with a specific level and formatter.

    :param handler_cls: The handler class to be instantiated (e.g., StreamHandler, FileHandler).
    :param level: The logging level for the handler.
    :param kwargs: Additional keyword arguments for the handler (e.g., filename for FileHandler).
    :return: Configured logging handler.
    """
    handler = handler_cls(**kwargs)
    handler.setLevel(level)
    formatter = get_formatter()
    handler.setFormatter(formatter)
    return handler


def get_formatter() -> Formatter:
    """
    Create and return a formatter for logging.

    :return: Configured formatter.
    """
    return Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
