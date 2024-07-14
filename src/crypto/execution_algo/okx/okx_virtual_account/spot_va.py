"""
Okx Virtual Account Management
"""

import os

import pandas as pd

from src.crypto.exchanges.okx.rest.okx_client import Okx
from src.crypto.execution_algo.okx.okx_virtual_account.virtual_account_config import (
    TRADING_ACCOUNT,
)
from src.libraries.logging.logger_client import LoggerClient


class VirtualAccount(Okx, LoggerClient):
    """
    Args:
        Okx (_type_): binance spot client
        LoggerClient (_type_): logging client
    """

    def __init__(self, apikey, apisecret, passphrase, file_path, file_name, save_mode):
        Okx.__init__(self, apikey, apisecret, passphrase)
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
                self.get_ticker({"instId": f"{symbol}-USDT"})["data"][0]["last"]
            )
        return price

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
                    user_assets = self.get_balance_funding()["data"][0]
                    self.logger.info(user_assets)
                    df = pd.DataFrame(user_assets, index=[0])
                    print(df)
                except Exception as e:
                    # print(e)
                    print("no balances")

            # trading account balance
            elif input_number == "2":
                print("pulling trading account balance")
                user_assets = self.get_balance_trading()["data"][0]["details"]
                self.logger.info(user_assets)
                df = pd.DataFrame(user_assets)
                df = df[["availBal", "availEq", "cashBal", "ccy", "uTime"]]
                print(df)

            # pull recent trades
            elif input_number == "3":
                input_symbol = input("Enter Okx Symbol e.g. BTC-USDT: ")
                recent_trades = self.get_transaction_details_3m(
                    {
                        "instType": "SPOT",
                        "instId": input_symbol.upper(),
                        "limit": 50,
                    }
                )

                if recent_trades["data"]:
                    self.logger.info(recent_trades)
                    df = pd.DataFrame(recent_trades["data"])
                    df = df[
                        [
                            "ordId",
                            "instId",
                            "side",
                            "fillSz",
                            "fillPx",
                            "fee",
                            "feeCcy",
                            "ts",
                        ]
                    ]
                    df["datetime"] = pd.to_datetime(df["ts"], unit="ms")
                    print(df)
                else:
                    print("no trades")

            # placing order
            elif input_number == "4":
                order_dict = {}
                base_ccy = input("Enter Base Currency: ").upper()
                quote_ccy = input("Enter Quote Currency: ").upper()

                order_dict["instId"] = f"{base_ccy}-{quote_ccy}"
                order_dict["tdMode"] = "cross"
                order_dict["side"] = input("Enter Direction, buy or sell: ").lower()
                order_dict["ordType"] = "limit"
                order_dict["sz"] = input("Enter Quantity - base qty only: ")
                order_dict["px"] = input("Enter Price: ")

                order_value = self.get_coin_value(base_ccy) * float(order_dict["sz"])

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
                open_orders = self.get_order_list()
                self.logger.info(open_orders)

                try:
                    df_open_orders = pd.DataFrame(open_orders["data"])
                    df_open_orders = df_open_orders[
                        [
                            "cTime",
                            "instId",
                            "ordId",
                            "ordType",
                            "px",
                            "side",
                            "sz",
                            "tdMode",
                        ]
                    ]
                    print(df_open_orders)
                except Exception as e:
                    print("no open orders")

            # cancel open order
            elif input_number == "6":
                order_symbol = input("Enter symbol e.g. BTC-USDT: ").upper()
                order_id = input("Enter orderId: ")
                cancel_order = self.cancel_order(
                    {
                        "instId": order_symbol,
                        "ordId": order_id,
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
        passphrase=TRADING_ACCOUNT["passphrase"],
        file_path=save_path,
        file_name=FILENAME,
        save_mode="a",
    )

    client.main()
