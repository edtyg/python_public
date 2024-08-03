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

from keys.api_work.messaging_apps.telegram import (
    HTS_bot1,
    HTS_bot2,
    HTS_bot3,
    HTS_bot4,
    HTS_bot5,
    HTS_bot6,
    HTS_bot7,
    HTS_bot8,
    HTS_bot9,
    HTS_bot10,
)


class Telegram:
    """
    Class to interact with telegram
    set up a telegram bot and add bot into chat groups

    using 1 unique bot per chat group - reduce rate limits
    """

    def __init__(self):
        self.telegram_base_url = "https://api.telegram.org/bot"
        self.timeout = 3

        ### emojis ###
        self.fire_emoji = "\U0001F525"
        self.alarm_emoji = "\U0001F6A8"

        self.bot1 = {
            "bot_name": HTS_bot1["bot_name"],
            "bot_token": HTS_bot1["bot_token"],
            "bot_grp_chat": HTS_bot1["bot_grp_chat"],
        }
        self.bot2 = {
            "bot_name": HTS_bot2["bot_name"],
            "bot_token": HTS_bot2["bot_token"],
            "bot_grp_chat": HTS_bot2["bot_grp_chat"],
        }
        self.bot3 = {
            "bot_name": HTS_bot3["bot_name"],
            "bot_token": HTS_bot3["bot_token"],
            "bot_grp_chat": HTS_bot3["bot_grp_chat"],
        }
        self.bot4 = {
            "bot_name": HTS_bot4["bot_name"],
            "bot_token": HTS_bot4["bot_token"],
            "bot_grp_chat": HTS_bot4["bot_grp_chat"],
        }
        self.bot5 = {
            "bot_name": HTS_bot5["bot_name"],
            "bot_token": HTS_bot5["bot_token"],
            "bot_grp_chat": HTS_bot5["bot_grp_chat"],
        }
        self.bot6 = {
            "bot_name": HTS_bot6["bot_name"],
            "bot_token": HTS_bot6["bot_token"],
            "bot_grp_chat": HTS_bot6["bot_grp_chat"],
        }
        self.bot7 = {
            "bot_name": HTS_bot7["bot_name"],
            "bot_token": HTS_bot7["bot_token"],
            "bot_grp_chat": HTS_bot7["bot_grp_chat"],
        }
        self.bot8 = {
            "bot_name": HTS_bot8["bot_name"],
            "bot_token": HTS_bot8["bot_token"],
            "bot_grp_chat": HTS_bot8["bot_grp_chat"],
        }
        self.bot9 = {
            "bot_name": HTS_bot9["bot_name"],
            "bot_token": HTS_bot9["bot_token"],
            "bot_grp_chat": HTS_bot9["bot_grp_chat"],
        }
        self.bot10 = {
            "bot_name": HTS_bot10["bot_name"],
            "bot_token": HTS_bot10["bot_token"],
            "bot_grp_chat": HTS_bot10["bot_grp_chat"],
        }

        self.chatbot_dict = {
            1: self.bot1,
            2: self.bot2,
            3: self.bot3,
            4: self.bot4,
            5: self.bot5,
            6: self.bot6,
            7: self.bot7,
            8: self.bot8,
            9: self.bot9,
            10: self.bot10,
        }

    def send_message(self, group_id: int, text_message: str):
        """Sends message to trade execution chat

        Args:
            group_id (int): 1 to 5 for now
            text_message (str): _description_
        """
        bot_credentials = self.chatbot_dict[group_id]
        url = self.telegram_base_url + bot_credentials["bot_token"]
        end_point = "/sendMessage"
        params = {
            "chat_id": bot_credentials["bot_grp_chat"],
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
                    timeout=self.timeout,
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

    def send_message_error(self, group_id: int, text: str):
        """
        sends a message in group chat when there's an error
        @users (mentions users directly that are in grp chat)
        """
        bot_credentials = self.chatbot_dict[group_id]
        url = self.telegram_base_url + bot_credentials["bot_token"]
        end_point = "/sendMessage"

        mention1 = "[rafael_hashkey](tg://user?id=" + str(5718686679) + ")"
        mention2 = "[Mark_HashKey](tg://user?id=" + str(5159647942) + ")"
        mention3 = "[edgartanhashkey](tg://user?id=" + str(6065963939) + ")"

        params = {
            "chat_id": bot_credentials["bot_grp_chat"],
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
                    timeout=self.timeout,
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
    client = Telegram()

    # sending normal message #
    resp = client.send_message(
        6,
        f"{client.fire_emoji*3} hi testing {client.fire_emoji*3}",
    )

    # # sending message with @users
    # resp = client.send_message_error(
    #     10,
    #     f"{client.fire_emoji*3} hi testing {client.fire_emoji*3}",
    # )
