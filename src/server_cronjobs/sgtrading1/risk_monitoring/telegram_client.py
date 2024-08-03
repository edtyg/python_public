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
        self.timeout = 5

        self.chatgroup_hts_chatbot = "-987081068"  # hts chatbot with gongye
        self.market_information_test = "-990460215"  # main group for chat notifications
        self.hts_algo_trade_executions = "-966990328"  # algo trade executions

        self.fire_emoji = "\U0001F525"
        self.alarm_emoji = "\U0001F6A8"

    def send_message(self, chat_group: str, text: str):
        """sends a message in group chat"""
        end_point = "sendMessage"
        params = {"chat_id": chat_group, "text": text}

        response = requests.get(
            self.base_url + end_point, params=params, timeout=self.timeout
        )
        return response


if __name__ == "__main__":
    client = Telegram()
    msg = client.send_message(
        client.chatgroup_hts_chatbot,
        f"{client.fire_emoji*5} hi testing {client.fire_emoji*5}",
    )
    print(msg)
