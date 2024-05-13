"""
deribit websocket connector
"""
import os

from python.projects.deribit_trading.slack_messager.slack_positions_messager import (
    SlackPositions,
)

if __name__ == "__main__":
    full_path = os.path.realpath(__file__)
    save_path = os.path.dirname(full_path) + "/"
    FILENAME = "btc_positions_slack.log"

    client = SlackPositions(save_path, FILENAME, "w")

    client.positions_slack("btc")
