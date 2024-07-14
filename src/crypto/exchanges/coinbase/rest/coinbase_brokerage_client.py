"""
https://docs.cdp.coinbase.com/advanced-trade/docs/welcome/
pip install coinbase-advanced-py
"""

from typing import Dict, Optional

import requests
from coinbase import jwt_generator


class CoinbaseBrokerage:
    """Coinbase Trading API
    Params for APIs can either be path or query
    """

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.coinbase_base_url = "https://api.coinbase.com"
        self.brokerage_endpoint = "/api/v3/brokerage"
        self.timeout = 3

    ######################
    ### json web token ###
    ######################

    # JWT expires after 2 minutes, after which all requests are unauthenticated.
    # You must generate a different JWT for each unique API request.

    def jwt_generator(self, method: str, path: str):
        """
        JSON Web Token Generator
        uses coinbase library to generate this

        Args:
            method (str): "GET" or "POST"
            path (str): "/api/v3/brokerage/accounts"
        """
        jwt_uri = jwt_generator.format_jwt_uri(method, path)
        jwt_token = jwt_generator.build_rest_jwt(jwt_uri, self.api_key, self.api_secret)
        return jwt_token

    ############################
    ### Standardized Methods ###
    ############################

    def _get(self, endpoint: str, params: Optional[Dict] = None):
        """
        GET Method

        Args:
            endpoint (str): /accounts
            params (Optional[Dict], optional)
        """
        token = self.jwt_generator("GET", self.brokerage_endpoint + endpoint)
        response = requests.get(
            self.coinbase_base_url + self.brokerage_endpoint + endpoint,
            headers={"Authorization": f"Bearer {token}"},
            params=params,
            timeout=self.timeout,
        )
        return response.json()

    def _post(self, endpoint: str, params: Optional[Dict] = None):
        """
        POST Method

        Args:
            endpoint (str): /accounts
            params (Optional[Dict], optional)
        """
        token = self.jwt_generator("POST", self.brokerage_endpoint + endpoint)
        response = requests.post(
            self.coinbase_base_url + self.brokerage_endpoint + endpoint,
            headers={"Authorization": f"Bearer {token}"},
            json=params,
            timeout=self.timeout,
        )
        return response.json()

    #########################
    ### API Methods Below ###
    #########################

    ################
    ### Accounts ###
    ################

    def list_accounts(self):
        """
        GET METHOD

        Get a list of authenticated accounts for the current user
        https://docs.cdp.coinbase.com/advanced-trade/reference/retailbrokerageapi_getaccounts/
        """
        endpoint = "/accounts"
        response = self._get(endpoint)
        return response

    def get_account(self, account_uuid: str):
        """
        GET METHOD

        Get a list of information about an account, given an account UUID.
        https://docs.cdp.coinbase.com/advanced-trade/reference/retailbrokerageapi_getaccount/

        Args:
            account_uuid: "9b7b204e-e9e8-5d42-98db-ccb0cc589e1a" - Path params
        """
        endpoint = f"/accounts/{account_uuid}"
        response = self._get(endpoint)
        return response

    ################
    ### Products ###
    ################

    def get_best_bid_ask(self, params: Optional[Dict] = None):
        """
        GET METHOD

        Get the best bid/ask for all products.
        subset of all products can be returned instead
        by using the product_ids input.
        https://docs.cdp.coinbase.com/advanced-trade/reference/retailbrokerageapi_getbestbidask/

        Args:
            params (Optional[Dict], optional): Defaults to None.
            {"product_ids": "BTC-USDT"}
        """
        endpoint = "/best_bid_ask"
        response = self._get(endpoint, params)
        return response

    def get_product_book(self, params: Optional[Dict] = None):
        """
        GET METHOD

        Get a list of bids/asks for a single product.
        The amount of detail shown can be customized with the limit parameter.
        https://docs.cdp.coinbase.com/advanced-trade/reference/retailbrokerageapi_getproductbook/

        Args:
            params (Optional[Dict], optional): Defaults to None.
            {"product_id": "BTC-USDT", "limit": 10}
        """
        endpoint = "/product_book"
        response = self._get(endpoint, params)
        return response

    def list_products(self):
        """
        GET METHOD

        Get a list of the available currency pairs for trading.
        https://docs.cdp.coinbase.com/advanced-trade/reference/retailbrokerageapi_getproducts/
        """
        endpoint = "/products"
        response = self._get(endpoint)
        return response

    def get_product(self, product_id: str):
        """
        GET METHOD

        Get information on a single product by product ID.
        https://docs.cdp.coinbase.com/advanced-trade/reference/retailbrokerageapi_getproduct/

        product_id = "BTC-USDT"
        """
        endpoint = f"/products/{product_id}"
        response = self._get(endpoint)
        return response

    def get_product_candles(self, product_id: str, params: dict):
        """
        GET METHOD

        Get rates for a single product by product ID, grouped in buckets.
        https://docs.cdp.coinbase.com/advanced-trade/reference/retailbrokerageapi_getcandles/

        product_id = "BTC-USDT"

        Args:
            params (dict):
            Name            Type        Mandatory   Description
            start           str         yes         1708408937
            end             str         yes         1708408937
            granularity     str         yes         ONE_MINUTE, ONE_HOUR, ONE_DAY
        """
        endpoint = f"/products/{product_id}/candles"
        response = self._get(endpoint, params=params)
        return response

    ##############
    ### Orders ###
    ##############

    def create_order(self, params: dict):
        """
        POST METHOD

        Create an order with a specified product_id (asset-pair), side (buy/sell)
        https://docs.cdp.coinbase.com/advanced-trade/reference/retailbrokerageapi_postorder/

        Args:
            params (dict):
            Name                Type        Mandatory   Description
            client_order_id     str         yes         unique client id
            product_id          str         yes         ticker e.g. "BTC-USDT"
            side                str         yes         "BUY" or "SELL"
            order_configuration dict        yes         config
            {"order_configuration": {"limit_limit_gtd": {"base_size": 1, "limit_price":1000}}}

        """
        endpoint = "/orders"
        response = self._post(endpoint, params)
        return response

    def cancel_orders(self, params: dict):
        """
        POST METHOD

        Initiate cancel requests for one or more orders.
        https://docs.cdp.coinbase.com/advanced-trade/reference/retailbrokerageapi_cancelorders/

        Args:
            params (dict):
            Name                Type        Mandatory   Description
            order_ids           list[str]         yes   existing order's id
        """
        endpoint = "/orders/batch_cancel"
        response = self._post(endpoint, params)
        return response

    ##################
    ### portfolios ###
    ##################

    def get_list_portfolios(self, params: dict = None):
        """
        GET METHOD

        Get a list of all portfolios of a user.
        https://docs.cdp.coinbase.com/advanced-trade/reference/retailbrokerageapi_getportfolios/

        Args:
            params (dict):
            Name                Type        Mandatory   Description
            portfolio_type      str         no
        """
        endpoint = "/portfolios"
        response = self._get(endpoint, params)
        return response

    def get_portfolio_breakdown(self, portfolio_uuid: str):
        """
        GET METHOD

        Get the breakdown of a portfolio by portfolio ID.
        https://docs.cdp.coinbase.com/advanced-trade/reference/retailbrokerageapi_getportfoliobreakdown/

        Args:
            params (dict):
            Name                Type        Mandatory   Description
            portfolio_type      str         no
        """
        endpoint = f"/portfolios/{portfolio_uuid}"
        response = self._get(endpoint)
        return response

    ##############
    ### Public ###
    ##############

    def get_market_trades(self, product_id: str, params: Optional[Dict] = None):
        """
        GET METHOD

        Get snapshot information by product ID about the last trades (ticks) and best bid/ask.
        https://docs.cdp.coinbase.com/advanced-trade/reference/retailbrokerageapi_getpublicmarkettrades/

        Args:
            params (dict):
            Name    Type        Mandatory   Description
            limit   int         yes
            start   str         no
            end     str         no
        """
        endpoint = f"/market/products/{product_id}/ticker"
        response = self._get(endpoint, params)
        return response
