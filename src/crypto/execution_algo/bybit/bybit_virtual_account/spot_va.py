"""
Okx Virtual Account Management
"""

import os

import pandas as pd

from src.crypto.exchanges.bybit.rest.bybit_client import Bybit
from src.crypto.execution_algo.bybit.bybit_virtual_account.virtual_account_config import (
    TRADING_ACCOUNT,
)
from src.libraries.logging.logger_client import LoggerClient


class VirtualAccount(Bybit, LoggerClient):
    """
    Args:
        Bybit (_type_): Bybit spot client
        LoggerClient (_type_): logging client
    """

    def __init__(self, apikey, apisecret, file_path, file_name, save_mode):
        Bybit.__init__(self, apikey, apisecret)
        LoggerClient.__init__(self, file_path, file_name, save_mode)

    def get_coin_value(self, symbol: str):
        """
        Args:
            symbol: 'BTC' or 'ETH' etc...

        returns symbol valuation in USDT terms, or 1 if stablecoin
        """
        stablecoin_list = ["USDT", "TUSD", "BUSD"]
        if symbol in stablecoin_list:
            price = 1
        else:
            data = self.get_tickers(
                {
                    "category": "spot",
                    "symbol": f"{symbol}USDT",
                }
            )
            price = data["result"]["list"][0]["lastPrice"]
        return float(price)

    #########################
    ### SPOT Account Here ###
    #########################

    def main(self):
        """
        Managing Okx Virtual account for Spot trades
        """

        status = True
        while status is True:
            print(
                """
                \nEnter 1 for Spot - Funding Acc Balance\
                \nEnter 2 for Spot - Trading Acc Balance\
                \nEnter 3 for Spot - Recent Trades\
                \nEnter 4 for Spot - Place Limit Order\
                \nEnter 5 for Spot - Check All Open Orders\
                \nEnter 6 for Spot - Close A Specific Open Order\
                \nEnter 0 to exit
                """
            )
            input_number = input("Enter Number: ")
            self.logger.info(f"number_entered={input_number}")

            # check if number is valid
            if input_number not in ["1", "2", "3", "4", "5", "6", "0"]:
                print("You did not enter a valid number, please try again")
                self.logger.warning("invalid_number_entered")
                continue

            # to exit loop
            if input_number == "0":
                print("Exiting")
                self.logger.info("exiting")
                status = False

            #########################
            ### Spot Methods Here ###
            #########################

            # funding account balance
            if input_number == "1":
                print("pulling funding account balance")
                try:
                    user_assets = self.get_all_coins_balance({"accountType": "FUND"})[
                        "result"
                    ]["balance"]
                    self.logger.info(user_assets)
                    df = pd.DataFrame(user_assets)
                    df["walletBalance"] = df["walletBalance"].astype("float")
                    df = df.loc[df["walletBalance"] > 0]
                    print(df)
                except Exception as e:
                    # print(e)
                    print("no balances")

            # trading account balance
            elif input_number == "2":
                print("pulling trading account balance")
                try:
                    user_assets = self.get_all_coins_balance(
                        {"accountType": "UNIFIED"}
                    )["result"]["balance"]
                    self.logger.info(user_assets)
                    df = pd.DataFrame(user_assets)
                    df["walletBalance"] = df["walletBalance"].astype("float")
                    df = df.loc[df["walletBalance"] != 0]
                    print(df)
                except Exception as e:
                    # print(e)
                    print("no balances")

            # pull recent trades
            elif input_number == "3":
                input_symbol = input("Enter BYBIT Symbol e.g. BTCUSDT: ")
                recent_trades = self.get_trade_history(
                    {
                        "category": "spot",
                        "symbol": input_symbol.upper(),
                        "limit": 10,
                    }
                )
                data = recent_trades["result"]["list"]
                df_data = pd.DataFrame(data)
                print(df_data)

            # placing order
            elif input_number == "4":
                order_dict = {}
                base_ccy = input("Enter Base Currency: ").upper()
                quote_ccy = input("Enter Quote Currency: ").upper()

                order_dict["category"] = "spot"
                order_dict["symbol"] = f"{base_ccy}{quote_ccy}"
                order_dict["isLeverage"] = 1
                order_dict["side"] = input("Enter Direction, Buy or Sell: ")
                order_dict["orderType"] = "limit"
                order_dict["qty"] = input("Enter Quantity - base qty only: ")
                order_dict["price"] = input("Enter Price: ")
                order_value = self.get_coin_value(base_ccy) * float(order_dict["qty"])

                # check if order value exceeds 5k
                print(f"Order Value = {order_value}")
                if order_value > 500000:
                    print("Order value > $500000 please change params")
                    self.logger.warning("order_value_exceeded")
                    continue

                print(order_dict)
                input_confirmation = input(
                    "Press 1 to confirm Parameters, Press 0 to cancel: "
                )

                if input_confirmation == "1":
                    limit_order = self.place_order(order_dict)
                    self.logger.info(limit_order)
                    print(limit_order)
                elif input_confirmation != "1":
                    self.logger.info("order_not_placed")
                    continue

            # check all open orders
            elif input_number == "5":
                input_symbol = input("Enter BYBIT Symbol e.g. BTCUSDT: ")
                open_orders = self.get_open_orders(
                    {
                        "category": "spot",
                        "symbol": input_symbol,
                    }
                )

                try:
                    df_open_orders = pd.DataFrame(open_orders["result"]["list"])
                    df_open_orders = df_open_orders[
                        [
                            "symbol",
                            "orderType",
                            "orderId",
                            "price",
                            "side",
                            "qty",
                        ]
                    ]
                    print(df_open_orders)
                except Exception as e:
                    print("no open orders")

            # cancel open order
            elif input_number == "6":
                order_symbol = input("Enter symbol e.g. BTCUSDT: ").upper()
                order_id = input("Enter orderId: ")
                cancel_order = self.cancel_order(
                    {
                        "category": "spot",
                        "symbol": order_symbol,
                        "orderId": order_id,
                    }
                )
                print(cancel_order)
                self.logger.info(cancel_order)


if __name__ == "__main__":
    # for saving logs
    full_path = os.path.realpath(__file__)
    save_path = os.path.dirname(full_path) + "/"
    FILENAME = "virtual_account_spot" + ".log"

    # initializing
    client = VirtualAccount(
        apikey=TRADING_ACCOUNT["api_key"],
        apisecret=TRADING_ACCOUNT["api_secret"],
        file_path=save_path,
        file_name=FILENAME,
        save_mode="a",
    )

    client.main()
