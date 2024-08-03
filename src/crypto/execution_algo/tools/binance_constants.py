"""
Binance Constants
"""

from strenum import LowercaseStrEnum


class BinanceConstants(LowercaseStrEnum):
    """
    this class serves to keep a list of constants from Binance API Responses
    """

    SYMBOL = "symbol"
    SYMBOLS = "symbols"
    PRICE = "price"
    FILTERS = "filters"
    TIMEZONE = "timeZone"
    SERVER_TIME = "serverTime"
    RATE_LIMITS = "rateLimits"
    TICKER = "ticker"
    STEP_SIZE = "stepSize"
    ASSET = "asset"
    FREE = "free"
    USER_ASSETS = "userAssets"
    NET_ASSET = "netAsset"
    STATUS = "status"
    ORDER_ID = "orderId"
    TRANSACT_TIME = "transactTime"
    SIDE = "side"
    FILLS = "fills"
    CUMULATIVE_QUOTE_QTY = "cummulativeQuoteQty"
    QUANTITY = "qty"
    MESSAGE = "msg"


# print(BinanceConstants.STATUS)
