# -*- coding: utf-8 -*-
"""
API docs here
https://lunarcrush.com/developers/api/endpoints
"""

import requests

from local_credentials.api_key_data import LUNARCRUSH_KEY_FREE


class LunarCrush:
    """rest api for lunarcrush - crypto text data"""

    def __init__(self, apikey):
        self.apikey = apikey
        self.base_url = "https://lunarcrush.com/api3"
        self.header = {"Authorization": f"Bearer {self.apikey}"}
        self.timeout = 5

    def get_coin_of_the_day(self):
        """gets coin of the day"""
        endpoint = "/coinoftheday"

        response = requests.get(
            self.base_url + endpoint, headers=self.header, timeout=self.timeout
        )
        data = response.json()
        return data


if __name__ == "__main__":
    client = LunarCrush(LUNARCRUSH_KEY_FREE)
    cotd = client.get_coin_of_the_day()
    print(cotd)
