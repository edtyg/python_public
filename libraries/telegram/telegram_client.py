import requests

from local_credentials.api_key_others import TELEGRAM_BOT_NAME, TELEGRAM_TOKEN


class telegram:
    def __init__(self):
        self.bot_name = TELEGRAM_BOT_NAME
        self.token = TELEGRAM_TOKEN
        self.base_url = f"https://api.telegram.org/bot{self.token}/"

        self.chat_id = "-435703625"  # crypto millionaire chat
        self.chat_id = "-829556349"  # 400m work chat

    def send_message(self, chat_id: str, text: str):
        end_point = "sendMessage"
        params = {"chat_id": chat_id, "text": text}

        r = requests.get(self.base_url + end_point, params=params)
        return r


if __name__ == "__main__":
    client = telegram()

    msg = client.send_message("-829556349", "hi testing")
