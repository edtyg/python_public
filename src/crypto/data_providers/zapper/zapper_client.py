# -*- coding: utf-8 -*-
"""
API docs here
https://studio.zapper.xyz/docs/apis/api-syntax#wallet-specific-app-and-erc20-token-balances-endpoints
"""

import requests

from local_credentials.api_key_data import ZAPPERFI_KEY_FREE


class Zapper:
    """rest api for zapper - wallet scanner"""

    def __init__(self, apikey):
        self.apikey = apikey
        self.base_url = "https://api.zapper.fi"
        self.header = {"Authorization": f"Bearer {self.apikey}"}
        self.timeout = 5


if __name__ == "__main__":
    client = Zapper(ZAPPERFI_KEY_FREE)
    cotd = client.get_coin_of_the_day()
    print(cotd)
