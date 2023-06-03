"""
sample script for creating logs
https://docs.python.org/3/library/logging.html#logrecord-attributes

5 levels of logging
"""
import logging
import os

full_path = os.path.realpath(__file__)
save_path = os.path.dirname(full_path) + "/"

logging.basicConfig(
    filename=save_path + "logging_example.log",
    level=logging.DEBUG,  # set default to DEBUG
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filemode="a",  # 'a' for append, 'w' for replace
)

# custom logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler("test.log")
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

try:
    1 / 0
except ZeroDivisionError as e:
    # can use to log errors
    logger.error("zerodivisionerror", exc_info=True)
    logger.exception("zerodivisionerror")
