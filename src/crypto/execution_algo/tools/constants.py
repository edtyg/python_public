"""
Constants
"""

from enum import auto

from strenum import LowercaseStrEnum


class Constants(LowercaseStrEnum):
    """
    this class serves to keep a list of constants used as inputs for
    the execution algos
    """

    # input params
    EXCHANGE = auto()
    ACCOUNT_NAME = auto()
    ALGO_TYPE = auto()
    BASE_CURRENCY = auto()
    QUOTE_CURRENCY = auto()
    TICKER = auto()
    DIRECTION = auto()
    CLIP_TYPE = auto()  # "base" or "quote"
    CLIP_LIMIT = auto()  # clip limit in USD terms
    QUANTITY = auto()  # trade quantity based on clip type
    TWAP_DURATION = auto()  # duration in seconds
    TWAP_CLIP_INTERVAL = auto()  # intervals between each clip in seconds
    ORDER_ID = auto()  # order id sent with each order
    LEVERAGE_RATIO = auto()  # for margin trades
    OTC_EXECUTION_PROPORTIONS = auto()
    PERCENTAGE_OF_VOLUME = auto()
    PERCENTAGE_OF_VOLUME_LOOKBACK = auto()
    POST_ONLY_CLIP_SIZE = auto()
    TELEGRAM_GROUP = auto()
    RANDOMIZER = auto()  # for randomizing clip sizes and sleep time
    TRADE_STATUS = auto()

    # calculated / derived params
    CLIP_CCY = auto()  # BTC if base, USDT if quote for BTC/USDT
    CLIP_COUNT = auto()  # number of twap orders
    CLIP_SIZE = auto()  # size of each order in "base" or "quote" currency
    CUMULATIVE_FILLED_BASE = auto()
    CUMULATIVE_FILLED_QUOTE = auto()
    REMAINING_BASE = auto()
    REMAINING_QUOTE = auto()
    REMAINING_TIME = auto()


class AlgoTypes(LowercaseStrEnum):
    """
    types of execution algos below

    using cross-margin account in binance
    UTA (Unified trading account) OKX and Bybit

    5 types of algos -> TWAP, VWAP, POV, POST ONLY, SPREAD_TRADING
    """

    TWAP_MARKET = "TWAP_MARKET"
    TWAP_MARKET_OTC = "TWAP_MARKET_OTC"
    TWAP_LIMIT = "TWAP_LIMIT"
    VWAP_MARKET = "VWAP_MARKET"
    POV_MARKET = "POV_MARKET"
    POST_LIMIT = "POST_ONLY"
    SPREAD_TRADING = "SPREAD_TRADING"


# for i in Constants:
#     print(i.value)
# print(list(Constants))
# print(list(AlgoTypes))
# print(Constants.ALGO_TYPE)
# print(Constants.ALGO_TYPE.value)
