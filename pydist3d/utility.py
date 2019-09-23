"""utility.py

Utility submodule for pydist3d

Contains logger

J. Metz <metz.jp@gmail.com>
"""
import logging
import coloredlogs

logger = logging.getLogger(__name__)
# Default format for coloredlogs is
# "%(asctime)s %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s"
coloredlogs.install(
    fmt="%(asctime)s %(name)s:%(lineno)d %(levelname)s %(message)s",
    level='DEBUG', logger=logger
)

