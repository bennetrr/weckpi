"""Utilitys for logging"""
import logging
import sys


def format_logger(logger: logging.Logger) -> None:
    """Apply formatting rules on the logger"""
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s | %(name)s] %(message)s')

    # The handler h1 logs only debug and info to stdout
    h1 = logging.StreamHandler(sys.stdout)
    h1.addFilter(lambda record: record.levelno <= logging.INFO)
    h1.setFormatter(formatter)

    # The handler h2 logs only warning, error and exception to stderr
    h2 = logging.StreamHandler()
    h2.setLevel(logging.WARNING)
    h2.setFormatter(formatter)

    logger.addHandler(h1)
    logger.addHandler(h2)
