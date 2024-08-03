"""
BYBIT Trading Algo
"""

from src.crypto.execution_algo.helper.helper_algo import HelperAlgo
from src.crypto.execution_algo.helper.helper_bybit import HelperBybit
from src.crypto.execution_algo.tools.constants import AlgoTypes, Constants


class BybitAlgoTrading(HelperBybit):
    """
    Args:
        HelperOkx: Helper client for common tasks
    """

    def __init__(self, api_key, api_secret, file_path, file_name, save_mode):
        HelperBybit.__init__(self, api_key, api_secret, file_path, file_name, save_mode)

    def bybit_trading_algo(self, order_params: dict) -> None | str:
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
            print("Selected Algo not in list, please check again")
            return

        print(
            f"BYBIT {trading_params[Constants.ALGO_TYPE]} {trading_params[Constants.DIRECTION]} order"
        )
        print(
            f"total quantity = {trading_params[Constants.QUANTITY]} {trading_params[Constants.CLIP_CCY]}"
        )
        print(f"order size on based on {trading_params[Constants.CLIP_TYPE]} currency")
        print("\n")

        # pulling balances and checking on valuation of balances
        base_ccy_balance = HelperBybit.get_spot_balance(
            self, trading_params[Constants.BASE_CURRENCY]
        )
        quote_ccy_balance = HelperBybit.get_spot_balance(
            self, trading_params[Constants.QUOTE_CURRENCY]
        )
        base_ccy_price = HelperBybit.get_spot_coin_price(
            self, trading_params[Constants.BASE_CURRENCY]
        )
        quote_ccy_price = HelperBybit.get_spot_coin_price(
            self, trading_params[Constants.QUOTE_CURRENCY]
        )
        print(f"{trading_params[Constants.BASE_CURRENCY]} price = {base_ccy_price}")
        print(f"{trading_params[Constants.QUOTE_CURRENCY]} price = {quote_ccy_price}")
        print(
            f"Account {trading_params[Constants.BASE_CURRENCY]} balance = {base_ccy_balance}"
        )
        print(
            f"Account {trading_params[Constants.QUOTE_CURRENCY]} balance = {quote_ccy_balance}"
        )
        account_valuation = (
            base_ccy_balance * base_ccy_price + quote_ccy_balance * quote_ccy_price
        )
        print(f"Account valuation = {round(account_valuation, 2)} USD")
        print(f"Leverage ratio = {trading_params[Constants.LEVERAGE_RATIO]}")
        account_valuation_leverage = (
            account_valuation * trading_params[Constants.LEVERAGE_RATIO]
        )
        print(
            f"Account valuation with leverage = {round(account_valuation_leverage,2)} USD"
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

        # 2 - Check if Ticker exists in OKX
        try:
            ticker_decimal_places = HelperBybit.get_ticker_info(
                self, "spot", trading_params[Constants.TICKER]
            )
        except KeyError:
            print("Ticker does not exist in OKX - please check again")
            return

        # 3 - Check on our balances - using margin calculation
        if (
            trading_params[Constants.DIRECTION] == "BUY"
            and trading_params[Constants.CLIP_TYPE] == "BASE"
        ):
            # Buying base ccy - Check if sufficient margin
            required_balance = base_ccy_price * trading_params[Constants.QUANTITY]
            if account_valuation_leverage < required_balance:
                print(f"insufficient margin. required margin = {required_balance} USD")
                return

        elif (
            trading_params[Constants.DIRECTION] == "BUY"
            and trading_params[Constants.CLIP_TYPE] == "QUOTE"
        ):
            # Buying quote ccy - Check if sufficient margin
            required_balance = quote_ccy_price * trading_params[Constants.QUANTITY]
            if account_valuation_leverage < required_balance:
                print(f"insufficient margin. required margin = {required_balance} USD")
                return

        elif (
            trading_params[Constants.DIRECTION] == "SELL"
            and trading_params[Constants.CLIP_TYPE] == "BASE"
        ):
            # Selling base ccy - Check if sufficient margin
            required_balance = base_ccy_price * trading_params[Constants.QUANTITY]
            if account_valuation_leverage < required_balance:
                print(f"insufficient margin. required margin = {required_balance} USD")
                return

        elif (
            trading_params[Constants.DIRECTION] == "SELL"
            and trading_params[Constants.CLIP_TYPE] == "QUOTE"
        ):
            # Selling quote ccy - Check if sufficient margin
            required_balance = quote_ccy_price * trading_params[Constants.QUANTITY]
            if account_valuation_leverage < required_balance:
                print(f"insufficient margin. required margin = {required_balance} USD")
                return

        ### Strategy Specific Checks ###
        if trading_params[Constants.ALGO_TYPE] == "TWAP_MARKET":
            HelperBybit.twap_market_order(self, trading_params)
        elif trading_params[Constants.ALGO_TYPE] == "TWAP_MARKET_OTC":
            HelperBybit.twap_market_otc_order(self, trading_params)
        elif trading_params[Constants.ALGO_TYPE] == "TWAP_LIMIT":
            HelperBybit.twap_limit_order(self, trading_params)
