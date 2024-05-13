"""
API DOCS here
https://cryptoquant.com/docs
Data calculated for all blocks produced in a day.
Each day begins at 00:00:00 UTC and end at 23:59:59 UTC
"""

import requests
from local_credentials.api_key_data import CRYPTOQUANT_KEY_PAID


class CryptoQuant:
    """
    cryptoquant's api are mainly split up into 4 branches:
    btc, eth, stablecoin and erc20 tokens
    """

    def __init__(self, apikey: str):
        self.apikey = apikey
        self.headers = {"Authorization": "Bearer" + " " + self.apikey}
        self.url = "https://api.cryptoquant.com/v1/"  # base url
        self.timeout = 5

    ###############
    ### methods ###
    ###############

    def get_endpoints(self) -> dict:
        """Gets all available api endpoints
        https://cryptoquant.com/docs#tag/Available-Endpoints

        Returns:
            df: [response from api call]
        """

        endpoint = "/discovery/endpoints"

        response = requests.get(
            self.url + endpoint, headers=self.headers, timeout=self.timeout
        )
        data = response.json()
        return data

    #####################
    ### BTC ENDPOINTS ###
    #####################

    # BTC Exchange Flows
    def get_btc_netflow(self, params: dict):
        """Gets exchange BTC Netflows
        https://cryptoquant.com/docs#operation/BTCgetExchangeNetflow

        Args:
            params (Dict):
        params      type    desc
        exchange    str     all_exchange, binance, ftx etc... this is required
        window      str     day, hour or block
        from        any     YYYYMMDDTHHMMSS 20191001T100000
        to          any     YYYYMMDDTHHMMSS 20201001T100000
        limit       integer [1, 100000] default = 100
        format      str     'json' or 'csv'
        """
        endpoint = "/btc/exchange-flows/netflow"
        response = requests.get(
            self.url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        return data

    def get_btc_inflow(self, params: dict):
        """Gets exchange BTC inflows
        https://cryptoquant.com/docs#operation/BTCgetInflow

        Args:
            params (Dict):

        params      type    desc
        exchange    str     all_exchange, binance, ftx etc... this is required
        window      str     day, hour or block
        from        any     YYYYMMDDTHHMMSS 20191001T100000
        to          any     YYYYMMDDTHHMMSS 20201001T100000
        limit       integer [1, 100000] default = 100
        format      str     'json' or 'csv'
        """
        endpoint = "/btc/exchange-flows/inflow"
        response = requests.get(
            self.url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        return data

    def get_btc_outflow(self, params: dict):
        """Gets exchange BTC Outflows
        https://cryptoquant.com/docs#operation/BTCgetOutflow

        Args:
            params (Dict):

        params      type    desc
        exchange    str     all_exchange, binance, ftx etc... this is required
        window      str     day, hour or block
        from        any     YYYYMMDDTHHMMSS 20191001T100000
        to          any     YYYYMMDDTHHMMSS 20201001T100000
        limit       integer [1, 100000] default = 100
        format      str     'json' or 'csv'
        """
        endpoint = "/btc/exchange-flows/outflow"
        response = requests.get(
            self.url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        return data

    #####################
    ### ETH ENDPOINTS ###
    #####################

    # ETH Exchange Flows
    def get_eth_netflow(self, params: dict):
        """Gets exchange ETH Netflows
        https://cryptoquant.com/docs#operation/ETHgetExchangeNetflow

        Args:
            params (Dict):

        params      type    desc
        exchange    str     all_exchange, binance, ftx etc... this is required
        window      str     day, hour or block
        from        any     YYYYMMDDTHHMMSS 20191001T100000
        to          any     YYYYMMDDTHHMMSS 20201001T100000
        limit       integer [1, 100000] default = 100
        format      str     'json' or 'csv'
        """
        endpoint = "/eth/exchange-flows/netflow"
        response = requests.get(
            self.url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        return data

    def get_eth_inflow(self, params: dict):
        """Gets exchange ETH inflows
        https://cryptoquant.com/docs#operation/ETHgetInflow

        Args:
            params (Dict):

        params      type    desc
        exchange    str     all_exchange, binance, ftx etc... this is required
        window      str     day, hour or block
        from        any     YYYYMMDDTHHMMSS 20191001T100000
        to          any     YYYYMMDDTHHMMSS 20201001T100000
        limit       integer [1, 100000] default = 100
        format      str     'json' or 'csv'
        """
        endpoint = "/eth/exchange-flows/inflow"
        response = requests.get(
            self.url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        return data

    def get_eth_outflow(self, params: dict):
        """Gets exchange ETH outflows
        https://cryptoquant.com/docs#operation/ETHgetOutflow

        Args:
            params (Dict):

        params      type    desc
        exchange    str     all_exchange, binance, ftx etc... this is required
        window      str     day, hour or block
        from        any     YYYYMMDDTHHMMSS 20191001T100000
        to          any     YYYYMMDDTHHMMSS 20201001T100000
        limit       integer [1, 100000] default = 100
        format      str     'json' or 'csv'
        """
        endpoint = "/eth/exchange-flows/outflow"
        response = requests.get(
            self.url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        return data

    #############################
    ### STABLECOINS ENDPOINTS ###
    #############################

    # Stablecoin Exchange flow
    def get_stablecoin_netflow(self, params: dict):
        """Gets Exchange stablecoin netflows
        https://cryptoquant.com/docs#operation/StablecoinGetExchangeNetflow

        Args:
            params (Dict):

        params      type    desc
        token       str     usdt_eth etc.. refer to stablecoin list
        exchange    str     all_exchange, binance, ftx etc... this is required
        window      str     day, hour or block
        from        any     YYYYMMDDTHHMMSS 20191001T100000
        to          any     YYYYMMDDTHHMMSS 20201001T100000
        limit       integer [1, 100000] default = 100
        format      str     'json' or 'csv'
        """
        endpoint = "/stablecoin/exchange-flows/netflow"
        response = requests.get(
            self.url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        return data

    def get_stablecoin_inflow(self, params: dict):
        """Gets exchange stablecoin inflows
        https://cryptoquant.com/docs#operation/StablecoinGetInflow

        Args:
            params (Dict):

        params      type    desc
        token       str     usdt_eth etc.. refer to stablecoin list
        exchange    str     all_exchange, binance, ftx etc... this is required
        window      str     day, hour or block
        from        any     YYYYMMDDTHHMMSS 20191001T100000
        to          any     YYYYMMDDTHHMMSS 20201001T100000
        limit       integer [1, 100000] default = 100
        format      str     'json' or 'csv'
        """
        endpoint = "/stablecoin/exchange-flows/inflow"
        response = requests.get(
            self.url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        return data

    def get_stablecoin_outflow(self, params: dict):
        """Gets exchange stablecoin outflows
        https://cryptoquant.com/docs#operation/StablecoinGetOutflow

        Args:
            params (Dict):

        params      type    desc
        token       str     usdt_eth etc.. refer to stablecoin list
        exchange    str     all_exchange, binance, ftx etc... this is required
        window      str     day, hour or block
        from        any     YYYYMMDDTHHMMSS 20191001T100000
        to          any     YYYYMMDDTHHMMSS 20201001T100000
        limit       integer [1, 100000] default = 100
        format      str     'json' or 'csv'
        """
        endpoint = "/stablecoin/exchange-flows/outflow"
        response = requests.get(
            self.url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        return data

    ########################
    ### ERC20  ENDPOINTS ###
    ########################

    # ERC20 Exchange Flow
    def get_erc20_netflow(self, params: dict):
        """Gets exchange erc20 coins netflows
        https://cryptoquant.com/docs#operation/ERC20GetExchangeNetflow

        Args:
            params (Dict):

        params      type    desc
        token       str     usdt_eth etc.. refer to stablecoin list
        exchange    str     all_exchange, binance, ftx etc... this is required
        window      str     day, hour or block
        from        any     YYYYMMDDTHHMMSS 20191001T100000
        to          any     YYYYMMDDTHHMMSS 20201001T100000
        limit       integer [1, 100000] default = 100
        format      str     'json' or 'csv'
        """

        endpoint = "/erc20/exchange-flows/netflow"

        response = requests.get(
            self.url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        return data

    def get_erc20_inflow(self, params: dict):
        """Gets exchange erc20 coins inflows
        https://cryptoquant.com/docs#operation/ERC20GetInflow

        Args:
            params (Dict):

        params      type    desc
        token       str     usdt_eth etc.. refer to stablecoin list
        exchange    str     all_exchange, binance, ftx etc... this is required
        window      str     day, hour or block
        from        any     YYYYMMDDTHHMMSS 20191001T100000
        to          any     YYYYMMDDTHHMMSS 20201001T100000
        limit       integer [1, 100000] default = 100
        format      str     'json' or 'csv'
        """
        endpoint = "/erc20/exchange-flows/inflow"
        response = requests.get(
            self.url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        return data

    def get_erc20_outflow(self, params: dict):
        """Gets exchange erc20 coins outflows
        https://cryptoquant.com/docs#operation/ERC20GetOutflow

        Args:
            params (Dict):

        params      type    desc
        token       str     usdt_eth etc.. refer to stablecoin list
        exchange    str     all_exchange, binance, ftx etc... this is required
        window      str     day, hour or block
        from        any     YYYYMMDDTHHMMSS 20191001T100000
        to          any     YYYYMMDDTHHMMSS 20201001T100000
        limit       integer [1, 100000] default = 100
        format      str     'json' or 'csv'
        """
        endpoint = "/erc20/exchange-flows/outflow"
        response = requests.get(
            self.url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        return data


if __name__ == "__main__":
    client = CryptoQuant(CRYPTOQUANT_KEY_PAID)

    endpoints = client.get_endpoints()
    print(endpoints)
