"""
OKX Constants
"""

from strenum import StrEnum


class OkxConstants(StrEnum):
    """
    this class serves to keep a list of constants from OKX API Responses
    """

    AVERAGE_PRICE = "avgPx"
    CASH_BALANCE = "cashBal"
    CURRENCY = "ccy"
    DATA = "data"
    DETAILS = "details"
    FILL_SIZE = "fillSz"
    FILL_TIME = "fillTime"
    FUTURES = "futures"
    INSTRUMENT_ID = "instId"
    INSTRUMENT_TYPE = "instType"
    LAST = "last"
    LOT_SIZE = "lotSz"
    MARGIN = "margin"
    MIN_SIZE = "minSz"
    OPTION = "option"
    SIDE = "side"
    SIZE = "sz"
    SPOT = "spot"
    SYMBOL = "symbol"
    SWAP = "swap"
    TARGET_CCY = "tgtCcy"
    TICK_SIZE = "tickSz"


# print(BinanceConstants.STATUS)
