"""
https://core.telegram.org/bots/api
Telegran API Docs here
"""
import requests


class Telegram:
    """Class to interact with telegram
    need to set up a telegram bot and add bot into chat groups
    """

    def __init__(self):
        self.bot_name = "@edtan_bot"
        self.token = "5949931630:AAH89e-ahxBbzmIG8GnkjuCYqM6CWYqH9jo"

        self.base_url = f"https://api.telegram.org/bot{self.token}/"

        self.chatgroup_400m = "-829556349"  # 400m work chat
        self.chatgroup_self = "-907566618"  # ed chat for testing
        self.chatgroup_hts_chatbot = "-987081068"  # hts chatbot with gongye

        self.timeout = 5

    def send_message(self, text: str):
        """sends a message in group chat"""
        end_point = "sendMessage"
        params = {"chat_id": self.chatgroup_hts_chatbot, "text": text}

        response = requests.get(
            self.base_url + end_point, params=params, timeout=self.timeout
        )
        print(response)
        return response


if __name__ == "__main__":
    client = Telegram()
    msg = client.send_message("hi testing")
