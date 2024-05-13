"""
CME datamine

https://www.cmegroup.com/market-data/datamine-api.html
"""

import requests

from local_credentials.api_personal.crypto_data.cme import CME_KEY


class CMEDATAMINE:
    """CME Datamine API"""

    def __init__(self, api_key: str, api_password: str):
        self.cme_base_url = "https://datamine.cmegroup.com/cme/api/v1/list"

        self.api_key = api_key
        self.api_password = api_password
        self.timeout = 5

    ##############
    ### Crypto ###
    ##############

    def get_crypto_data(self):
        """
        cme crypto data
        """
        params = {"dataset": "cryptocurrency", "yyyymmdd": "20240301"}

        response = requests.get(
            self.cme_base_url,
            params=params,
            timeout=self.timeout,
            auth=(self.api_key, self.api_password),
        )
        data = response.json()
        return data


if __name__ == "__main__":
    account = CME_KEY
    client = CMEDATAMINE(CME_KEY["api_key"], CME_KEY["api_password"])

    data = client.get_crypto_data()
    print(data)
