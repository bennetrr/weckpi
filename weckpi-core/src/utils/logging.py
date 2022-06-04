"""Utilitys for logging"""
import logging
import sys


def format_logger(logger: logging.Logger) -> None:
    """Apply formatting rules on the logger"""
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[{levelname} | {name}] {message}', style='{')

    # The handler h1 logs only debug and info to stdout
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.addFilter(lambda record: record.levelno <= logging.INFO)
    stdout_handler.setFormatter(formatter)

    # The handler h2 logs only warning, error and exception to stderr
    stderr_handler = logging.StreamHandler()
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)
