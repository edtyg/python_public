"""
Kraken api docs here
https://docs.kraken.com/api/docs/category/rest-api/market-data

Only writing for Public APIs
"""

from typing import Dict, Optional

import requests
from requests.exceptions import HTTPError, RequestException, Timeout


class Kraken:
    """
    Kraken Rest API - Public API Calls
    """

    def __init__(self):
        self.kraken_base_url = "https://api.kraken.com/0"
        self.timeout = 5

    #############################
    ### General Requests here ###
    #############################

    def rest_requests(
        self,
        request_type: str,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
    ):
        """Rest requests with error handling

        Args:
            request_type (str): either public or private api calls
            method (str): get, post, delete -> commonly used methods
            base_url (str): binance base url endpoint -> differs for spot, margin, futures
            endpoint (str): endpoint of your api call
            params (Optional[Dict]): params for your api call if required
        """

        if request_type.upper() not in ["PUBLIC", "PRIVATE"]:
            print("Invalid request type: has to be public or private")
            return

        if method.upper() not in ["GET", "POST", "DELETE", "PUT"]:
            print("Invalid Request Method")
            return

        try:
            if request_type.upper() == "PRIVATE":
                resp = requests.request(
                    method=method,
                    url=self.kraken_base_url + endpoint,
                    params=params,
                    timeout=self.timeout,
                )
            elif request_type.upper() == "PUBLIC":
                resp = requests.request(
                    method=method,
                    url=self.kraken_base_url + endpoint,
                    params=params,
                    timeout=self.timeout,
                )

            return resp.json()

        except HTTPError as http_error:
            # 404 or 500 error
            print(f"HTTP Error: {http_error}")

        except Timeout as timeout_error:
            # Request timed out
            print(f"Request Timed out: {timeout_error}")

        except RequestException as request_error:
            # Other requests error
            print(f"Request error: {request_error}")

        except ValueError as json_error:
            # Json decoding error
            print(f"JSON decode error: {json_error}")

        except Exception as error:
            # other exceptions
            print(f"An unexpected error occurred: {error}")

    ###################
    ### Market Data ###
    ###################

    def get_asset_info(self, params: Optional[Dict] = None) -> dict:
        """
        PUBLIC GET request
        https://docs.kraken.com/api/docs/rest-api/get-asset-info

        Get information about the assets that are available for deposit, withdrawal, trading and earn.

        Args:
            params (dict):
            Name                Type        Mandatory   Description
            asset 	            str 	    no          Example: XBT,ETH
            aclass   	        str 	    no          Example: currency
        """
        endpoint = "/public/Assets"
        return self.rest_requests("PUBLIC", "GET", endpoint, params)

    def get_tradable_pairs(self, params: Optional[Dict] = None) -> dict:
        """
        PUBLIC GET request
        https://docs.kraken.com/api/docs/rest-api/get-tradable-asset-pairs

        Get tradable asset pairs

        Args:
            params (dict):
            Name                Type        Mandatory   Description
            pair 	            str 	    no          Example: BTC/USD,ETH/BTC
            info       	        str 	    no          [info, leverage, fees, margin]
            country_code        str         no          Example: US:TX,GB,CA
        """
        endpoint = "/public/AssetPairs"
        return self.rest_requests("PUBLIC", "GET", endpoint, params)

    def get_ticker_info(self, params: Optional[Dict] = None) -> dict:
        """
        PUBLIC GET request
        https://docs.kraken.com/api/docs/rest-api/get-ticker-information

        Get tradable asset pairs

        Args:
            params (dict):
            Name                Type        Mandatory   Description
            pair 	            str 	    No          Example: XBTUSD
        """
        endpoint = "/public/Ticker"
        return self.rest_requests("PUBLIC", "GET", endpoint, params)

    def get_ohlc_data(self, params: Optional[Dict] = None) -> dict:
        """
        PUBLIC GET request
        https://docs.kraken.com/api/docs/rest-api/get-ohlc-data

        GET OHLC information. The last entry in the OHLC array is for the current,
        not-yet-committed frame and will always be present,
        regardless of the value of since.

        Return up to 720 OHLC data points since given timestamp

        Args:
            params (dict):
            Name        Type        Mandatory   Description
            pair 	    str 	    yes         Example: XBTUSD
            interval    int         yes         Possible values: [1, 5, 15, 30, 60, 240, 1440, 10080, 21600]
            since       int         no          Example: 1548111600
        """
        endpoint = "/public/OHLC"
        return self.rest_requests("PUBLIC", "GET", endpoint, params)

    def get_recent_trades(self, params: Optional[Dict] = None) -> dict:
        """
        PUBLIC GET request
        https://docs.kraken.com/api/docs/rest-api/get-recent-trades

        Returns the last 1000 trades by default

        Args:
            params (dict):
            Name        Type        Mandatory   Description
            pair 	    str 	    yes         Example: XBTUSD
            since       int         no          Example: 1548111600
            count       int         no          Example: 2, up to 1000
        """
        endpoint = "/public/Trades"
        return self.rest_requests("PUBLIC", "GET", endpoint, params)
