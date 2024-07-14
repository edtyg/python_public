"""
sample script for creating logs
https://docs.python.org/3/library/logging.html#logrecord-attributes

5 levels of logging
DEBUG, INFO, WARNING, ERROR, CRITICAL
"""

import logging
import os


class LoggerClient:
    """A class method for setting up logs"""

    def __init__(self, file_path: str, file_name: str, save_mode: str):
        self.filepath = file_path
        self.filename = file_name
        self.mode = save_mode

        logging.basicConfig(
            filename=self.filepath + self.filename,
            level=logging.INFO,
            format="%(asctime)s.%(msecs)03d|filename=%(module)s.py|line=%(lineno)d|pid=%(process)d|level=%(levelname)s|message=%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            filemode=self.mode,
        )
        self.logger = logging.getLogger(__name__)


if __name__ == "__main__":
    full_path = os.path.realpath(__file__)
    save_path = os.path.dirname(full_path) + "/"
    FILENAME = "testing.log"

    client = LoggerClient(save_path, FILENAME, "a")
    client.logger.info("testing")
