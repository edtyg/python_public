"""
Constants
"""

from enum import auto

from strenum import LowercaseStrEnum, UppercaseStrEnum


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
    PRICE = auto()
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


class AlgoTypes(UppercaseStrEnum):
    """
    types of execution algos below

    using cross-margin account in binance (SPOT)
    UTA (Unified trading account) OKX and Bybit
    """

    TWAP_MARKET = auto()
    TWAP_MARKET_OTC = auto()
    TWAP_LIMIT = auto()
    VWAP_MARKET = auto()
    POV_MARKET = auto()
    POST_LIMIT = auto()
    SPREAD_TRADING = auto()


class Exchanges(UppercaseStrEnum):
    """
    Crypto Exchanges
    """

    BINANCE = auto()
    OKX = auto()
    BYBIT = auto()


class Accounts(UppercaseStrEnum):
    """
    Exchange Accounts
    """

    BINANCE_MCA_MAIN_TRADE = auto()

    OKX_MCA_MAIN_TRADE = auto()
    OKX_MCA_LTP1_TRADE = auto()

    BYBIT_MCA_MAIN_TRADE = auto()
    BYBIT_MCA_LTP1_TRADE = auto()
