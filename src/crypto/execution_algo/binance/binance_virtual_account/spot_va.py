"""
Binance Virtual Account Management - Spot
"""

import os

import pandas as pd

from src.crypto.exchanges.binance.rest.binance_spot import BinanceSpot
from src.crypto.execution_algo.binance.binance_virtual_account.virtual_account_config import (
    TRADING_ACCOUNT,
)
from src.libraries.logging.logger_client import LoggerClient


class VirtualAccount(BinanceSpot, LoggerClient):
    """
    Args:
        BinanceSpot (_type_): binance spot client
        LoggerClient (_type_): logging client
    """

    def __init__(self, apikey, apisecret, file_path, file_name, save_mode):
        BinanceSpot.__init__(self, apikey, apisecret)
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
            price = float(
                self.get_symbol_price_ticker({"symbol": f"{symbol}USDT"})["price"]
            )
        return price

    #########################
    ### SPOT Account Here ###
    #########################

    def main(self):
        """
        Managing Binance Virtual account for Spot trades
        """

        status = True
        while status is True:
            print(
                "\nEnter 1 for Spot - Balances\
                \nEnter 2 for Spot - Recent Trades\
                \nEnter 3 for Spot - Place Limit Order\
                \nEnter 4 for Spot - Check All Open Orders\
                \nEnter 5 for Spot - Close A Specific Open Order\
                \nEnter 6 for Spot - Close All Open Orders\
                \n\
                \nEnter 0 to exit"
            )
            input_number = input("Enter Number: ")
            self.logger.info(f"number_entered={input_number}")

            # check if number is valid
            if input_number not in [
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "0",
            ]:
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

            # checking spot balances
            if input_number == "1":
                print("pulling spot balances")
                user_assets = self.post_user_asset()
                self.logger.info(user_assets)
                try:
                    df = pd.DataFrame(user_assets)
                    df = df[["asset", "free", "locked", "freeze", "withdrawing"]]
                    print(df)
                except Exception as e:
                    print(e)

            # pull recent trades
            elif input_number == "2":
                input_symbol = input("Enter Binance Symbol: ")
                recent_trades = self.get_account_trade_list(
                    {"symbol": input_symbol.upper(), "limit": 5}
                )
                print(recent_trades)
                if type(recent_trades) is dict and recent_trades["code"] == -1121:
                    self.logger.warning(recent_trades)
                    print("Invalid Symbol, please try again")
                elif type(recent_trades) is list and recent_trades:
                    self.logger.info(recent_trades)
                    df = pd.DataFrame(recent_trades)
                    df["datetime"] = pd.to_datetime(df["time"], unit="ms")
                    print(df)
                else:
                    print("no recent trades")

            # placing order
            elif input_number == "3":
                order_dict = {}
                base_ccy = input("Enter Base Currency: ").upper()
                quote_ccy = input("Enter Quote Currency: ").upper()
                order_dict["symbol"] = base_ccy + quote_ccy
                order_dict["side"] = input("Enter Direction: ").upper()
                order_dict["type"] = "LIMIT"
                order_dict["quantity"] = input("Enter Quantity: ").upper()
                order_dict["price"] = input("Enter Price: ").upper()
                order_dict["timeInForce"] = "GTC"
                order_value = self.get_coin_value(base_ccy) * float(
                    order_dict["quantity"]
                )

                # check if order value exceeds 10mil
                print(f"Order Value = {order_value}")
                if order_value > 10_000_000:
                    print("Order value > $10_000_000 please change params")
                    self.logger.warning("order_value_exceeded")
                    continue

                print(order_dict)
                input_confirmation = input(
                    "Press 1 to confirm Parameters, Press 0 to cancel: "
                )

                if input_confirmation == "1":
                    limit_order = self.post_order(order_dict)
                    self.logger.info(limit_order)
                    print(limit_order)
                elif input_confirmation != "1":
                    self.logger.info("order_not_placed")
                    continue

            # check open orders
            elif input_number == "4":
                open_orders = self.get_current_open_orders()
                self.logger.info(open_orders)

                if open_orders:
                    df_open_orders = pd.DataFrame(open_orders)
                    print(df_open_orders)
                else:
                    print(open_orders)

            # close open order
            elif input_number == "5":
                order_symbol = input("Enter Symbol: ").upper()
                order_id = input("Enter orderId: ")
                cancel_order = self.delete_order(
                    {"symbol": order_symbol, "orderId": order_id}
                )
                print(cancel_order)
                self.logger.info(cancel_order)

            # close all open orders
            elif input_number == "6":
                order_symbol = input("Enter Symbol: ").upper()
                cancel_all_orders = self.delete_all_open_orders(
                    {"symbol": order_symbol}
                )
                print(cancel_all_orders)
                self.logger.info(cancel_all_orders)


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
