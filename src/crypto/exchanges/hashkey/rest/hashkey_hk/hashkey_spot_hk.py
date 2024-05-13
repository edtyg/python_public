"""
Spot APis here
"""

from typing import Dict, Optional

from local_credentials.api_personal.crypto_exchanges.hashkey import HASHKEY_TRADE
from python.crypto.exchanges.hashkey.rest.hashkey_hk.hashkey_client_hk import (
    HashkeyExchange,
)


class HashkeySpot(HashkeyExchange):
    """
    Hashkey Exchange Spot Child class
    """

    def __init__(self, api_key: str, api_secret: str):
        super().__init__(api_key, api_secret)

    ########################
    ### Order Management ###
    ########################

    def post_create_order(self, params: dict) -> dict:
        """Signed API call
        Create a single order request to Exchange
        https://hashkeypro-apidoc.readme.io/reference/create-order

        Args:
            params (Optional[Dict], optional): Defaults to None
            PARAMETER   TYPE    REQUIRED    DESCRIPTION
            symbol	            STRING	Y	        Name of instrument "BTCUSD"
            side	            ENUM	Y	        BUY or SELL
            type	            ENUM	Y	        Currently offer 3 order types:
                                                    LIMIT
                                                    MARKET
                                                    LIMIT_MAKER
            quantity	        DECIMAL	Y	        Order amount - base qty
            amount	            DECIMAL		        Cash amount - quote currency.
                                                    Market order only. (To be released)
            price	            DECIMAL	C	        Required for LIMIT and LIMIT_MAKER order
            newClientOrderId	STRING		        self-generated order id
            timeInForce	        ENUM		        GTC for Limit order and IOC for Market order
            timestamp	        LONG		        Timestamp in Milliseconds

        Returns:
            dict
        """
        endpoint = "/api/v1/spot/order"
        response = self._get_private(endpoint, params)
        return response

    def delete_cancel_order(self, params: dict) -> dict:
        """Signed API call
        Cancel an existing order. Either orderId or clientOrderId must be sent.
        https://hashkeypro-apidoc.readme.io/reference/cancel-order

        Args:
            params (Optional[Dict], optional): Defaults to None
            PARAMETER       TYPE    REQUIRED    DESCRIPTION
            orderId	        LONG		        Order ID
            clientOrderId	STRING		        client order id

        Returns:
            dict
        """
        endpoint = "/api/v1/spot/order"
        response = self._delete_signed(endpoint, params)
        return response

    def get_current_open_orders(self, params: Optional[Dict] = None) -> dict:
        """Signed API call
        Query current active orders
        https://hashkeypro-apidoc.readme.io/reference/get-current-open-orders

        Args:
            params (Optional[Dict], optional): Defaults to None
            PARAMETER       TYPE    EXAMPLE_VALUES      DESCRIPTION
            orderId	        LONG    1470930457684189696	Order ID
            symbol	        STRING	BTCUSD	            Currency pair
            limit	        INT		20	                Default 500, Maximum 1000

        Returns:
            dict
        """
        endpoint = "/api/v1/spot/openOrders"
        response = self._get_private(endpoint, params)
        return response

    def get_all_traded_orders(self, params: Optional[Dict] = None) -> dict:
        """Signed API call
        Retrieve all traded orders
        https://hashkeypro-apidoc.readme.io/reference/get-all-orders

        Args:
            params (Optional[Dict], optional): Defaults to None
            PARAMETER       TYPE    REQUIRED    DESCRIPTION
            orderId	        LONG		        Order ID
            symbol	        STRING		        Currency pair
            startTime	    LONG		        Start Timestamp
            endTime	        LONG		        End Timestamp
            limit	        INT		            Default 500, max 1000

        Returns:
            dict
        """
        endpoint = "/api/v1/spot/tradeOrders"
        response = self._get_private(endpoint, params)
        return response

    ###############
    ### Account ###
    ###############

    def get_vip_info(self):
        """Signed API Call
        Retrieve VIP Level and Trading fee rates
        https://hashkeypro-apidoc.readme.io/reference/get-vip-info
        """
        endpoint = "/api/v1/account/vipInfo"
        response = self._get_private(endpoint)
        return response

    def get_account_info(self, params: Optional[Dict] = None) -> dict:
        """Signed API call
        Retrieve account balance
        https://hashkeypro-apidoc.readme.io/reference/get-account-information

        Args:
            params (Optional[Dict], optional): Defaults to None
            PARAMETER   TYPE    REQUIRED    DESCRIPTION
            accountId   LONG    YES         Account ID, for Master Key only

        Returns:
            dict: {'balances': [{'asset': 'BTC', 'assetId': 'BTC', 'assetName': 'BTC',
                                'total':'901.5', 'free': '901.5', 'locked': '0'}],
                                'userId': '1533385456787692288'}
        """
        endpoint = "/api/v1/account"
        response = self._get_private(endpoint, params)
        return response

    def get_account_trade_list(self, params: Optional[Dict] = None) -> dict:
        """Signed API call
        Query account history and transaction records
        https://hashkeypro-apidoc.readme.io/reference/get-account-trade-list

        Args:
            params (Optional[Dict], optional): Defaults to None
            PARAMETER       TYPE    REQUIRED    DESCRIPTION
            symbol	        STRING		        Trading pair
            startTime	    LONG		        Start Timestamp
            endTime	        LONG		        End Timestamp
            clientOrderId	STRING		        Client Order ID
            fromId	        LONG		        Starting ID
            toId	        LONG		        End ID
            limit	        INT		            Limit of record

        Returns:
            dict
        """
        endpoint = "/api/v1/account/trades"
        response = self._get_private(endpoint, params)
        return response

    def get_query_account_type(self, params: Optional[Dict] = None) -> dict:
        """Signed API call
        https://hashkeypro-apidoc.readme.io/reference/query-sub-account

        Args:
            params (Optional[Dict], optional): Defaults to None
            PARAMETER       TYPE    REQUIRED    DESCRIPTION
            accountType	    STRING		        Trading pair

        Returns:
            dict
        """
        endpoint = "/api/v1/account/type"
        response = self._get_private(endpoint, params)
        return response

    ### wallet ###
    def get_deposit_address(self, params: Dict) -> dict:
        """Signed API call
        Retrieve deposit address generated by the system
        https://hashkeypro-apidoc.readme.io/reference/get-deposit-address

        Args:
            params (Optional[Dict], optional): Defaults to None
            PARAMETER   TYPE    REQUIRED    EXAMPLE VALUES  DESCRIPTION
            coin	    STRING	Y	        USDT	        Coin name
            chainType	ENUM	Y	        ETH	            Chain Type

        Returns:
            dict:
        """
        endpoint = "/api/v1/account/deposit/address"
        response = self._get_private(endpoint, params)
        return response


if __name__ == "__main__":
    account = HASHKEY_TRADE
    client = HashkeySpot(account["api_key"], account["api_secret"])

    # custody account id: 1468013748774110721
    # fiat account id: 1468013748774110722
    # main trading account id: 1468013748774110720
    # OPT account id: 1468177790721468160

    # fee_tier = client.get_vip_info()
    # print(fee_tier)

    acc_info = client.get_account_info()
    print(acc_info)

    # custody_account = client.get_account_info({"accountId": "1468013748774110721"})
    # print(custody_account)

    # fiat_account = client.get_account_info({"accountId": "1468013748774110722"})
    # print(fiat_account)
