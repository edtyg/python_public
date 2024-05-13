"""
https://core.telegram.org/bots/api
Telegran API Docs here
"""

import requests

from local_credentials.api_personal.messaging_apps.telegram import (
    edtan_bot1,
    edtan_bot2,
    edtan_bot3,
    edtan_bot4,
    edtan_bot5,
)


class Telegram:
    """
    Class to interact with telegram
    need to set up a telegram bot and add bot into chat groups
    initialize with bot token and chat id
    """

    def __init__(self, bot_token: str, bot_chat_id: str):
        self.bot_token = bot_token
        self.bot_chat_id = bot_chat_id

        self.bot_base_url = f"https://api.telegram.org/bot{self.bot_token}/"
        self.timeout = 3

    def send_message_bot(self, text: str):
        """sends a message in group chat"""
        end_point = "sendMessage"
        params = {
            "chat_id": self.bot_chat_id,
            "text": text,
        }
        response = requests.get(
            self.bot_base_url + end_point,
            params=params,
            timeout=self.timeout,
        )
        return response


if __name__ == "__main__":
    bot_credentials = edtan_bot5
    client = Telegram(
        bot_credentials["bot_token"],
        bot_credentials["bot_grp_chats"]["edtan_testing5"],
    )
    msg = client.send_message_bot("hi testing")
