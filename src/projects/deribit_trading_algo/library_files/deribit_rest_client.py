"""
client to interact with deribit's api
"""
import base64
import pandas as pd
import requests

from local_credentials.api_key_exchanges import DERIBIT_KEY, DERIBIT_SECRET


class DeribitRestClient:
    """
    A Python wrapper for the Deribit REST API.

    Args:
        apikey (str): The API key to authenticate requests.
        apisecret (str): The API secret to authenticate requests.

    Attributes:
        apikey (str): The API key used for authentication.
        apisecret (str): The API secret used for authentication.
        base_url (str): The base URL for the Deribit REST API.
        auth_params (dict): The authentication parameters used in requests.
        headers (dict): The headers used in requests.

    """

    def __init__(self, apikey: str, apisecret: str):
        self.apikey = apikey
        self.apisecret = apisecret

        self.base_url = "https://www.deribit.com/api/v2"
        self.auth_params = {
            "client_id": self.apikey,
            "client_secret": self.apisecret,
            "grant_type": "client_credentials",
        }
        self.headers = {
            "Authorization": f'Basic {self.base64(self.apikey + ":" + self.apisecret)}'
        }
        self.timeout = 10

    def base64(self, message):
        """does a base64 encoding for your message"""
        message_bytes = message.encode("ascii")
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode("ascii")
        return base64_message

    ###################
    ### market data ###
    ###################

    def get_currencies(self, params: dict = None):
        """Retrieves all cryptocurrencies supported by the API."""
        endpoint = "/public/get_currencies"
        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        return response.json()

    def get_delivery_prices(self, params: dict):
        """Retrives delivery prices for then given index.

        Args:
            params (dict):
            Parameter 	Required 	Type 	Enum
            index_name 	true 	    string 	btc_usd, eth_usd
            offset      false       integer
            count       false       integer
        """
        endpoint = "/public/get_delivery_prices"
        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        return response.json()

    def get_instruments(self, params: dict):
        """Retrieves available trading instruments.
        This method can be used to see which instruments are available for
        trading, or which instruments have recently expired.

        Args:
            params (dict):
            Parameter 	Required 	Type 	Enum
            currency 	true 	    string 	BTC, ETH, SOL, USDC
            kind        false       string  future, option
            expired     false       boolean
        """
        endpoint = "/public/get_instruments"
        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        return response.json()

    def get_last_settlements_by_instrument(self, params: dict):
        """Retrieves historical public settlement, delivery
        and bankruptcy events filtered by instrument name.

        Args:
            params (dict):
            Parameter 	            Required 	Type
            instrument_name 	    true 	    string
            type 	                false 	    string
            count 	                false 	    integer
            continuation 	        false 	    string
            search_start_timestamp 	false 	    integer
        """
        endpoint = "/public/get_last_settlements_by_instrument"
        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        return response.json()

    def get_order_book(self, params: dict):
        """Retrieves the order book, along with other market values for
        a given instrument.

        Args:
            params (dict):
            Parameter 	            Required 	Type
            instrument_name 	    true 	    string
            depth 	                false 	    number
        """
        endpoint = "/public/get_order_book"
        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        return response.json()

    ###############
    ### trading ###
    ###############

    def place_buy_order(self, params: dict):
        """Places a buy order for an instrument.

        Args:
            params (dict):
            Parameter 	        Required 	Type 	    Enum
            instrument_name 	true 	    string
            amount              true        number
            type                false       string      limit, market
            label               false       string
            price               false       number
            time_in_force       false       string      good_til_cancelled
            post_only           false       boolean
            reduce_only         false       boolean
        """
        endpoint = "/private/buy"
        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )  # signed request
        return response.json()

    def place_sell_order(self, params: dict):
        """Places a sell order for an instrument.

        Args:
            params (dict):
            Parameter 	        Required 	Type 	    Enum
            instrument_name 	true 	    string
            amount              true        number
            type                false       string      limit, market
            label               false       string
            price               false       number
            time_in_force       false       string      good_til_cancelled
            post_only           false       boolean
            reduce_only         false       boolean
        """
        endpoint = "/private/sell"
        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )  # signed request
        return response.json()

    def edit_order(self, params: dict):
        """Change price, amount and/or other properties of an order.

        Args:
            params (dict):
            Parameter 	        Required 	Type 	    Enum
            order_id         	true 	    string
            amount              true        number
            price               false       number
            post_only           false       boolean
            reduce_only         false       boolean
        """
        endpoint = "/private/edit"
        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )  # signed request
        return response.json()

    def cancel_order(self, params: dict):
        """Cancel an order, specified by order id

        Args:
            params (dict):
            Parameter 	        Required 	Type
            order_id         	true 	    string
        """
        endpoint = "/private/cancel"
        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )  # signed request
        return response.json()

    def get_order_state(self, params: dict):
        """Change price, amount and/or other properties of an order.

        Args:
            params (dict):
            Parameter 	        Required 	Type
            order_id         	true 	    string
        """
        endpoint = "/private/get_order_state"
        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )  # signed request
        return response.json()

    def get_user_trades_by_currency(self, params: dict):
        """Retrieve the latest user trades that have occurred for
        instruments in a specific currency symbol.

        Args:
            params (dict):
            Parameter 	Required 	Type
            currency 	true 	    string
            kind        false       string
            start_id    false       string
            end_id      false       string
            count       false       integer
            include_old false       boolean
            sorting     false       string
        """

        endpoint = "/private/get_user_trades_by_currency"
        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )  # signed request
        return response.json()

    def get_user_trades_by_instrument(self, params: dict):
        """Retrieve the latest user trades that have
        occurred for a specific instrument.

        Args:
            params (dict):
            Parameter 	        Required 	Type 	    Enum
            instrument_name     true        string
            count               false       integer
            include_old         false       boolean
            sorting             false       string      asc, desc, default
        """

        endpoint = "/private/get_user_trades_by_instrument"
        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )  # signed request
        return response.json()

    ###############
    ### wallets ###
    ###############

    def get_deposits(self, params: dict):
        """Retrieve the latest users deposits

        Args:
            params (dict):
            Parameter 	        Required 	Type 	    Enum
            currency            true        string      BTC,ETH,SOL,USDC
            count               false       integer
        """

        endpoint = "/private/get_deposits"
        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )  # signed request
        return response.json()

    def get_transfers(self, params: dict):
        """Retrieve the user's transfers list

        Args:
            params (dict):
            Parameter 	        Required 	Type 	    Enum
            currency            true        string      BTC,ETH,SOL,USDC
            count               false       integer
        """

        endpoint = "/private/get_transfers"
        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )  # signed request
        return response.json()

    def get_withdrawals(self, params: dict):
        """Retrieve the latest users withdrawals

        Args:
            params (dict):
            Parameter 	        Required 	Type 	    Enum
            currency            true        string      BTC,ETH,SOL,USDC
            count               false       integer
        """

        endpoint = "/private/get_withdrawals"
        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )  # signed request
        return response.json()

    ##########################
    ### account management ###
    ##########################

    def get_account_summary(self, currency_symbol: str):
        """_summary_

        Args:
            currency_symbol (str): 'btc' or 'eth'

        Returns:
            _type_: _description_
        """
        endpoint = "/private/get_account_summary"
        params = {"currency": currency_symbol}

        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )  # signed request
        data = response.json()

        return data

    def get_positions(self, currency_symbol: str):
        """_summary_

        Args:
            currency_symbol (str): 'btc' or 'eth'

        Returns:
            _type_: _description_
        """
        endpoint = "/private/get_positions"
        params = {"currency": currency_symbol}

        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )  # signed request
        data = response.json()

        return data

    def get_transaction_log(
        self, currency: str, start_timestamp: int, end_timestamp: int
    ):
        """_summary_

        Args:
            currency_symbol (str): 'btc' or 'eth'

        Returns:
            _type_: _description_
        """
        endpoint = "/private/get_transaction_log"
        params = {
            "currency": currency,
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
        }

        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )  # signed request
        data = response.json()

        return data


if __name__ == "__main__":
    client = DeribitRestClient(DERIBIT_KEY, DERIBIT_SECRET)
    acc_summary = client.get_account_summary("eth")

    pos = client.get_positions("eth")
    df = pd.DataFrame(pos["result"])
    print(df)
