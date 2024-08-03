"""
Binance Trading Algo
"""

from src.crypto.execution_algo.helper.helper_algo import HelperAlgo
from src.crypto.execution_algo.helper.helper_binance import HelperBinance
from src.crypto.execution_algo.tools.constants import AlgoTypes, Constants


class BinanceAlgoTrading(HelperBinance):
    """
    Args:
        HelperBinance: Helper client for common tasks
    """

    def __init__(self, api_key, api_secret, file_path, file_name, save_mode):
        HelperBinance.__init__(
            self, api_key, api_secret, file_path, file_name, save_mode
        )

    def binance_trading_algo(self, order_params: dict) -> None | str:
        """
        Checks algo and places order

        Args:
            order_params: dict

        Returns:
            either returns None if checks fail
            or a string "checks_passed" if checks passes
        """
        trading_params = HelperAlgo.params_parser(order_params)
        print(trading_params)

        ##############################
        ### conducting some checks ###
        ##############################

        # check on algo type
        if trading_params[Constants.ALGO_TYPE] not in list(AlgoTypes):
            print(f"Selected Algo not in list, select the following {list(AlgoTypes)}")
            return

        print(
            f"BINANCE {trading_params[Constants.ALGO_TYPE]} {trading_params[Constants.DIRECTION]} order"
        )
        print(
            f"total quantity = {trading_params[Constants.QUANTITY]} {trading_params[Constants.CLIP_CCY]}"
        )
        print(f"order size on based on {trading_params[Constants.CLIP_TYPE]} currency")
        print("\n")

        # pulling balances and checking on valuation of balances
        base_ccy_price = HelperBinance.get_spot_coin_price(
            self, trading_params[Constants.BASE_CURRENCY]
        )
        quote_ccy_price = HelperBinance.get_spot_coin_price(
            self, trading_params[Constants.QUOTE_CURRENCY]
        )
        cm_base_ccy_balance = HelperBinance.get_cross_margin_balance(
            self, trading_params[Constants.BASE_CURRENCY]
        )
        cm_quote_ccy_balance = HelperBinance.get_cross_margin_balance(
            self, trading_params[Constants.QUOTE_CURRENCY]
        )
        print(f"{trading_params[Constants.BASE_CURRENCY]} price = {base_ccy_price}")
        print(f"{trading_params[Constants.QUOTE_CURRENCY]} price = {quote_ccy_price}")
        print(
            f"Cross Margin {trading_params[Constants.BASE_CURRENCY]} balance = {cm_base_ccy_balance}"
        )
        print(
            f"Cross Margin {trading_params[Constants.QUOTE_CURRENCY]} balance = {cm_quote_ccy_balance}"
        )
        cm_valuation = (
            cm_base_ccy_balance * base_ccy_price
            + cm_quote_ccy_balance * quote_ccy_price
        )
        print(f"Cross Margin valuation = {round(cm_valuation, 2)} USD")
        print(f"leverage ratio = {trading_params[Constants.LEVERAGE_RATIO]}")
        cm_valuation_leverage = cm_valuation * trading_params[Constants.LEVERAGE_RATIO]
        print(
            f"Cross Margin valuation with leverage = {round(cm_valuation_leverage,2)} USD"
        )
        print("conducting some checks")
        print("\n")

        ### Generic Checks ###
        # 1 - Check if Ticker keyed in correctly
        if (
            trading_params[Constants.TICKER]
            != trading_params[Constants.BASE_CURRENCY]
            + trading_params[Constants.QUOTE_CURRENCY]
        ):
            print("Please check on ticker, does not match base and quote ccy")
            return

        # 2 - Check if Ticker exists in Binance
        try:
            ticker_decimal_places = HelperBinance.get_spot_ticker_info(
                self, trading_params[Constants.TICKER]
            )
        except KeyError:
            print("Ticker does not exist in Binance - please check again")
            return

        # 3 - Check on our balances - using margin calculation
        if (
            trading_params[Constants.DIRECTION] == "BUY"
            and trading_params[Constants.CLIP_TYPE] == "BASE"
        ):
            # Buying base ccy - Check if sufficient margin
            required_balance = base_ccy_price * trading_params[Constants.QUANTITY]
            if cm_valuation_leverage < required_balance:
                print(f"insufficient margin. required margin = {required_balance} USD")
                return

        elif (
            trading_params[Constants.DIRECTION] == "BUY"
            and trading_params[Constants.CLIP_TYPE] == "QUOTE"
        ):
            # Buying quote ccy - Check if sufficient margin
            required_balance = quote_ccy_price * trading_params[Constants.QUANTITY]
            if cm_valuation_leverage < required_balance:
                print(f"insufficient margin. required margin = {required_balance} USD")
                return

        elif (
            trading_params[Constants.DIRECTION] == "SELL"
            and trading_params[Constants.CLIP_TYPE] == "BASE"
        ):
            # Selling base ccy - Check if sufficient margin
            required_balance = base_ccy_price * trading_params[Constants.QUANTITY]
            if cm_valuation_leverage < required_balance:
                print(f"insufficient margin. required margin = {required_balance} USD")
                return

        elif (
            trading_params[Constants.DIRECTION] == "SELL"
            and trading_params[Constants.CLIP_TYPE] == "QUOTE"
        ):
            # Selling quote ccy - Check if sufficient margin
            required_balance = quote_ccy_price * trading_params[Constants.QUANTITY]
            if cm_valuation_leverage < required_balance:
                print(f"insufficient margin. required margin = {required_balance} USD")
                return

        ### Strategy Specific Checks ###
        if trading_params[Constants.ALGO_TYPE] == "TWAP_MARKET":
            HelperBinance.twap_market_order(self, trading_params)
        elif trading_params[Constants.ALGO_TYPE] == "TWAP_MARKET_OTC":
            HelperBinance.twap_market_otc_order(self, trading_params)
        elif trading_params[Constants.ALGO_TYPE] == "TWAP_LIMIT":
            HelperBinance.twap_limit_order(self, trading_params)
