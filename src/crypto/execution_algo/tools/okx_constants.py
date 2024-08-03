"""
OKX Constants
"""

from strenum import LowercaseStrEnum


class OkxConstants(LowercaseStrEnum):
    """
    this class serves to keep a list of constants from OKX API Responses
    """

    MIN_SIZE = "minSz"
    DATA = "data"
    INSTRUMENT_TYPE = "instType"
    INSTRUMENT_ID = "instId"
    SPOT = "spot"
    SYMBOL = "symbol"
    DETAILS = "details"
    CURRENCY = "ccy"
    CASH_BALANCE = "cashBal"
    TARGET_CCY = "tgtCcy"
    SIZE = "sz"
    FILL_TIME = "fillTime"
    SIDE = "side"
    FILL_SIZE = "fillSz"
    AVERAGE_PRICE = "avgPx"


# print(BinanceConstants.STATUS)
