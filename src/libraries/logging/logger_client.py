"""
sample script for creating logs
https://docs.python.org/3/library/logging.html#logrecord-attributes

5 levels of logging
"""

import logging
import os

full_path = os.path.realpath(__file__)
save_path = os.path.dirname(full_path) + "/"

# class LoggerClient
logging.basicConfig(
    filename=save_path + "test.log",
    level=logging.DEBUG,  # set default to DEBUG
    format="""
        %(asctime)s.%(msecs)03d\
        |filename=%(module)s.py\
        |line=%(lineno)d\
        |pid=%(process)d\
        |level=%(levelname)s\
        |message=%(message)s\
        """.replace(
        " ", ""
    ),
    datefmt="%Y-%m-%d %H:%M:%S",
    filemode="a",  # a for append, w for write/replace
)
logger = logging.getLogger(__name__)
logger.debug("debug message")
