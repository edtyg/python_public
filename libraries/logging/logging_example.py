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
    format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filemode="a",  # 'a' for append, 'w' for replace
)

logging.debug("debug message")
logging.info("info message ")
logging.warning("warning message")
logging.error("error message")
logging.critical("critical message")
