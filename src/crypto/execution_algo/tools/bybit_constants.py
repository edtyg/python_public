"""
OKX Constants
"""

from strenum import StrEnum


class BybitConstants(StrEnum):
    """
    this class serves to keep a list of constants from OKX API Responses
    """

    ACCOUNT_TYPE = "accountType"
    AVERAGE_PRICE = "avgPrice"
    BALANCE = "balance"
    BASE_PRECISION = "basePrecision"
    CATEGORY = "category"
    COIN = "coin"
    CUMULATIVE_BASE = "cumExecQty"
    CUMULATIVE_QUOTE = "cumExecValue"
    DATA = "data"
    INVERSE = "inverse"
    LAST_PRICE = "lastPrice"
    LINEAR = "linear"
    LIST = "list"
    LOT_SIZE_FILTER = "lotSizeFilter"
    MARKET_UNIT = "marketUnit"
    MIN_ORDER_AMT = "minOrderAmt"
    MIN_ORDER_QTY = "minOrderQty"
    OPTION = "option"
    ORDER_ID = "ordId"
    PRICE_FILTER = "priceFilter"
    QUANTITY = "qty"
    QUOTE_PRECISION = "quotePrecision"
    RESULT = "result"
    SIDE = "side"
    SPOT = "spot"
    SYMBOL = "symbol"
    TICK_SIZE = "tickSize"
    UPDATED_TIME = "updatedTime"
    UNIFIED = "UNIFIED"
    WALLET_BALANCE = "walletBalance"
