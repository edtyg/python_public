"""
Telegram client for posting trade execution messages

https://core.telegram.org/bots/api
Telegran API Docs here

Rate Limits:
< 30 messages per second,
< 20 messages per min to 1 group
"""

import time

import requests

from keys.api_work.messaging_apps.telegram import TELEGRAM_ALGO_TRADING


class TelegramMessenger:
    """
    Class to interact with telegram
    set up a telegram bot and add bot into chat groups

    using 1 unique bot per chat group - reduce rate limits
    """

    telegram_base_url = "https://api.telegram.org/bot"
    timeout = 3

    ### emojis ###
    fire_emoji = "\U0001F525"
    alarm_emoji = "\U0001F6A8"

    @staticmethod
    def send_message(group_id: int, text_message: str):
        """Sends message to Telegram Algo Trading Group Chat

        Args:
            group_id (int): 1 to 5 for now
            text_message (str): _description_
        """
        bot_name = f"TRADING_BOT{group_id}"
        bot_credentials = TELEGRAM_ALGO_TRADING[bot_name]
        bot_token = bot_credentials["bot_token"]
        bot_chat_group = bot_credentials["bot_grp_chat"]

        url = TelegramMessenger.telegram_base_url + bot_token
        end_point = "/sendMessage"
        params = {
            "chat_id": bot_chat_group,
            "text": text_message,
        }

        # try a few times
        count = 0
        message_sent_status = False
        while message_sent_status is False:
            try:
                response = requests.get(
                    url + end_point,
                    params=params,
                    timeout=TelegramMessenger.timeout,
                )
                if count >= 5:
                    print("Exiting Loop")
                    message_sent_status = True
                    continue

                if response.status_code == 400:
                    print(response)

                elif response.status_code == 200:
                    message_sent_status = True
                    return response

            except Exception as error:
                print(error)
                print("sleeping tg bot")
                time.sleep(0.1)

            count += 1
            print(f"count = {count}")

        return response

    @staticmethod
    def send_message_error(group_id: int, text: str):
        """
        sends a message in group chat when there's an error
        @users (mentions users directly that are in grp chat)
        """
        bot_name = f"TRADING_BOT{group_id}"
        bot_credentials = TELEGRAM_ALGO_TRADING[bot_name]
        bot_token = bot_credentials["bot_token"]
        bot_chat_group = bot_credentials["bot_grp_chat"]

        url = TelegramMessenger.telegram_base_url + bot_token
        end_point = "/sendMessage"

        mention1 = "[rafael_hashkey](tg://user?id=" + str(5718686679) + ")"
        mention2 = "[Mark_HashKey](tg://user?id=" + str(5159647942) + ")"
        mention3 = "[edgartanhashkey](tg://user?id=" + str(6065963939) + ")"
        params = {
            "chat_id": bot_chat_group,
            "text": f"{mention1} {mention2} {mention3} {text}",
            "parse_mode": "Markdown",
        }

        # try a few times
        count = 0
        message_sent_status = False
        while message_sent_status is False:
            try:
                response = requests.get(
                    url + end_point,
                    params=params,
                    timeout=TelegramMessenger.timeout,
                )
                if count >= 5:
                    print("Exiting Loop")
                    message_sent_status = True
                    continue

                if response.status_code == 400:
                    print(response)

                elif response.status_code == 200:
                    print(response)
                    message_sent_status = True
                    return response

            except Exception as error:
                print(error)
                print("sleeping tg bot")
                time.sleep(0.1)

            count += 1
            print(f"count = {count}")

        return response


if __name__ == "__main__":

    # sending normal message
    resp = TelegramMessenger.send_message(
        5,
        f"{TelegramMessenger.fire_emoji*3} hi testing {TelegramMessenger.fire_emoji*3}",
    )

    # sending message with @users
    resp = TelegramMessenger.send_message_error(
        10,
        f"{TelegramMessenger.fire_emoji*3} hi testing {TelegramMessenger.fire_emoji*3}",
    )
