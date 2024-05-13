"""
to read logs
"""

import os

full_path = os.path.realpath(__file__)
save_path = os.path.dirname(full_path) + "/"
filename = "test.log"

if __name__ == "__main__":
    filepath = save_path + filename

    with open(filepath, "r") as log_file:
        for line in log_file:
            print(line.split("|"))
