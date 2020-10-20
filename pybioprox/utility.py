"""utility.py

Utility submodule for pybioprox

Contains logger

J. Metz <metz.jp@gmail.com>
"""
import inspect
import logging
import coloredlogs


def get_logger(name=None):
    """
    Returns a logger for the current module
    """
    if name is None:
        name = inspect.getmodule(inspect.currentframe().f_back).__name__
    logger = logging.getLogger(name)
    # Default format for coloredlogs is
    # "%(asctime)s %(hostname)s %(name)s[%(process)d]
    # ... %(levelname)s %(message)s"
    coloredlogs.install(
        fmt="%(asctime)s %(name)s:%(lineno)d %(levelname)s %(message)s",
        level='DEBUG', logger=logger
    )
    return logger
