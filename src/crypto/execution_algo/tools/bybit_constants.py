"""
OKX Constants
"""

from strenum import LowercaseStrEnum


class BybitConstants(LowercaseStrEnum):
    """
    this class serves to keep a list of constants from OKX API Responses
    """

    CATEGORY = "category"
    SYMBOL = "symbol"
    RESULT = "result"
    LIST = "list"
    BASE_PRECISION = "basePrecision"
    LOT_SIZE_FILTER = "lotSizeFilter"
    # RESULT = "result"
    LAST_PRICE = "lastPrice"
    QUANTITY = "qty"
    MARKET_UNIT = "marketUnit"
    DATA = "data"
    ORDER_ID = "ordId"
    UPDATED_TIME = "updatedTime"
    SIDE = "side"
    CUMULATIVE_BASE = "cumExecQty"
    AVERAGE_PRICE = "avgPrice"


# print(BybitConstants.RESULT)
