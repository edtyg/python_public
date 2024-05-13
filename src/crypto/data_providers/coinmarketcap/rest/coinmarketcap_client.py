"""
API Docs
https://coinmarketcap.com/api/documentation/v1/
"""

from typing import Dict, Optional

import requests


class CoinMarketCap:
    """Coinmarketcap Rest api"""

    def __init__(self, apikey: str):
        self.apikey = apikey
        self.cmc_base_url = "https://pro-api.coinmarketcap.com"

        self.headers = {"X-CMC_PRO_API_KEY": self.apikey}
        self.timeout = 5

    ###########################
    ### Standard get method ###
    ###########################

    def _get(self, endpoint: str, params: Optional[Dict] = None):
        """
        Standard GET Request
        No POST requests for Coinmarketcap
        """

        try:
            if params is None:
                response = requests.get(
                    self.cmc_base_url + endpoint,
                    headers=self.headers,
                    timeout=self.timeout,
                )
            elif params is not None:
                response = requests.get(
                    self.cmc_base_url + endpoint,
                    headers=self.headers,
                    params=params,
                    timeout=self.timeout,
                )
            return response.json()

        except requests.exceptions.Timeout:
            print("Request timed out. Please try again later.")
            return None

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    ######################
    ### Cryptocurrency ###
    ######################

    def get_airdrops(self, params: Optional[Dict] = None):
        """Get Airdrops data
        https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyAirdrops

        Args:
            params (dict):
            NAME                TYPE        MANDATORY   DESCRIPTION
            start	            int	        no          Optionally offset the start
            limit	            int	        no          default = 100
            status      	    str         no          default = "ONGOING"
                                                        valid = "ENDED" "ONGOING" "UPCOMING"
            id                  str         no          cmc coin id Example: 1
            slug                str         no          Example: "bitcoin"
            symbol              str         no          Example: "BTC"
        """
        endpoint = "/v1/cryptocurrency/airdrops"
        return self._get(endpoint, params)

    def get_cmc_id_map(self, params: Optional[Dict] = None):
        """Get list of id for all crypto from coinmarketcap
        https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyMap

        Args:
            params (dict):
            NAME                TYPE        MANDATORY   DESCRIPTION
            listing_status	    str	        no          default = "active
            start               int         no          offset the start
            limit	            int	        no          default = 100
            sort                str         no          default = "id" "cmc_rank"
            symbol              str         no          Example: "BTC"
            aux                 str         no
        """
        endpoint = "/v1/cryptocurrency/map"
        return self._get(endpoint, params)

    def get_ohlcv_historical_v2(self, params: dict):
        """Get historical ohlcv v2
        https://coinmarketcap.com/api/documentation/v1/#operation/getV2CryptocurrencyOhlcvHistorical

        Params:
            name                type    desc
            id                  string  coinmaketcap crypto id e.g. 1, 1027
            slug                string  e.g. bitcoin, ethereum
            symbol              string  e.g. btc
            time_period         string  e.g. daily, hourly
            time_start          string  e.g. 2018-09-19
            time_end            string  e.g. 2018-09-19
            count               int     1...10000 default = 10
            interval            string  hourly, daily
            convert             str     default = "USD"
            convert_id          str     convert by id
        """
        endpoint = "/v2/cryptocurrency/ohlcv/historical"
        return self._get(endpoint, params)
