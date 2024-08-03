"""
Class to help with logs - creating and reading

Logging Levels
CRITICAL (50): Indicates a very serious error, potentially preventing the program from continuing to run.
ERROR (40): Indicates a more severe problem, leading to program failure in some way.
WARNING (30): Indicates a potential issue or something unexpected, or is used to highlight some event that is of interest.
INFO (20): Provides general information about program execution, such as progress or state changes.
DEBUG (10): Provides detailed information, useful during development for diagnosing issues.
"""

import ast
import logging
import os

import pandas as pd


class LoggerHelper:
    """
    Helper class to work with log files
    """

    def __init__(self, file_path: str, file_name: str, save_mode: str):
        self.filepath = file_path
        self.filename = file_name
        self.mode = save_mode

        logging.basicConfig(
            filename=self.filepath + self.filename,
            level=logging.INFO,
            format="%(asctime)s.%(msecs)03d|filename=%(module)s.py|line=%(lineno)d|pid=%(process)d|level=%(levelname)s|message=%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            filemode=self.mode,
        )
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def parse_binance_trade_logs(log_file_path: str):
        """
        parses trading logs for binance
        """

        # loops through log file appends messages that we're able to split
        msg_data = []
        with open(log_file_path, "r", encoding="UTF-8") as log_file:
            for line in log_file:
                try:
                    msg_split = line.split("|")
                    message = msg_split[5]
                    msg_data.append(message)
                except Exception as e:
                    print(e)

        data_parsed = []
        for msg in msg_data:
            try:
                parsing_msg = msg[8:]
                data_dict = ast.literal_eval(parsing_msg)
                data_parsed.append(data_dict)
            except Exception as e:
                print(e)

        # appends as dataframe
        df_data_fills = pd.DataFrame()
        for dict_data in data_parsed:
            # sample data -> can have multiple fills
            # {
            #     "symbol": "BTCUSDT",
            #     "orderId": 28114986016,
            #     "clientOrderId": "opt-btc",
            #     "transactTime": 1719385470110,
            #     "price": "0",
            #     "origQty": "0.00008",
            #     "executedQty": "0.00008",
            #     "cummulativeQuoteQty": "4.92368",
            #     "status": "FILLED",
            #     "timeInForce": "GTC",
            #     "type": "MARKET",
            #     "side": "BUY",
            #     "fills": [
            #         {
            #             "price": "61546",
            #             "qty": "0.00008",
            #             "commission": "0.00000002",
            #             "commissionAsset": "BTC",
            #             "tradeId": 3651037978,
            #         }
            #     ],
            #     "isIsolated": False,
            #     "selfTradePreventionMode": "EXPIRE_MAKER",
            # }
            try:
                transact_time = dict_data["transactTime"]
                order_id = dict_data["orderId"]
                symbol = dict_data["symbol"]
                client_id = dict_data["clientOrderId"]
                fills = dict_data["fills"]

                # get fills
                df_data = pd.DataFrame(fills)
                df_data["transact_time"] = transact_time
                df_data["order_id"] = order_id
                df_data["symbol"] = symbol
                df_data["client_id"] = client_id

                df_data_fills = pd.concat([df_data_fills, df_data])

            except Exception as e:
                print(e)
                continue

        # final adjustments
        df_data_fills["datetime"] = pd.to_datetime(
            df_data_fills["transact_time"], unit="ms"
        )
        df_data_fills["price"] = df_data_fills["price"].astype("float")
        df_data_fills["qty"] = df_data_fills["qty"].astype("float")
        df_data_fills["volume"] = df_data_fills["price"] * df_data_fills["qty"]
        df_data_fills.reset_index(drop=True, inplace=True)
        print(df_data_fills)
        return df_data_fills

    @staticmethod
    def parse_bybit_trade_logs(log_file_path: str):
        """
        parses trading logs for bybit
        """

        # loops through log file appends messages that we're able to split
        msg_data = []
        with open(log_file_path, "r", encoding="UTF-8") as log_file:
            for line in log_file:
                try:
                    msg_split = line.split("|")
                    message = msg_split[5]
                    msg_data.append(message)
                except Exception as e:
                    print(e)

        data_parsed = []
        for msg in msg_data:
            try:
                parsing_msg = msg[8:]
                data_dict = ast.literal_eval(parsing_msg)
                data_parsed.append(data_dict)
            except Exception as e:
                print(e)
        print(data_parsed)

        # appends as dataframe
        df_data_fills = pd.DataFrame()
        for dict_data in data_parsed:
            # sample data -> can have multiple fills
            # {
            #     "retCode": 0,
            #     "retMsg": "OK",
            #     "result": {
            #         "nextPageCursor": "3154855%3A0%2C3154855%3A0",
            #         "category": "spot",
            #         "list": [
            #             {
            #                 "symbol": "BTCUSDT",
            #                 "orderType": "Market",
            #                 "underlyingPrice": "",
            #                 "orderLinkId": "test_1719821211",
            #                 "orderId": "1720379445568867328",
            #                 "stopOrderType": "",
            #                 "execTime": "1719821211464",
            #                 "feeCurrency": "USDT",
            #                 "feeRate": "0.00015",
            #                 "tradeIv": "",
            #                 "blockTradeId": "",
            #                 "markPrice": "",
            #                 "execPrice": "63311.9",
            #                 "markIv": "",
            #                 "orderQty": "0.000023",
            #                 "orderPrice": "61412.55",
            #                 "execValue": "1.3928618",
            #                 "closedSize": "",
            #                 "execType": "Trade",
            #                 "seq": 33083036412,
            #                 "side": "Sell",
            #                 "indexPrice": "",
            #                 "leavesQty": "0.000001",
            #                 "isMaker": False,
            #                 "execFee": "0.00020892927",
            #                 "execId": "2290000000234990741",
            #                 "marketUnit": "quoteCoin",
            #                 "execQty": "0.000022",
            #             }
            #         ],
            #     },
            #     "retExtInfo": {},
            #     "time": 1719821212110,
            # }
            try:
                res = dict_data["result"]
                fills = res["list"]

                # get fills
                df_data = pd.DataFrame(fills)
                df_data_fills = pd.concat([df_data_fills, df_data])

            except Exception as e:
                continue

        # final adjustments
        df_data_fills["datetime"] = pd.to_datetime(df_data_fills["execTime"], unit="ms")
        df_data_fills["execPrice"] = df_data_fills["execPrice"].astype("float")
        df_data_fills["execQty"] = df_data_fills["execQty"].astype("float")
        df_data_fills["volume"] = df_data_fills["execPrice"] * df_data_fills["execQty"]
        df_data_fills.reset_index(drop=True, inplace=True)
        return df_data_fills

    @staticmethod
    def parse_okx_trade_logs(log_file_path: str):
        """
        parses trading logs for okx
        """

        # loops through log file appends messages that we're able to split
        msg_data = []
        with open(log_file_path, "r", encoding="UTF-8") as log_file:
            for line in log_file:
                try:
                    msg_split = line.split("|")
                    message = msg_split[5]
                    msg_data.append(message)
                except Exception as e:
                    print(e)

        data_parsed = []
        for msg in msg_data:
            try:
                parsing_msg = msg[8:]
                data_dict = ast.literal_eval(parsing_msg)
                data_parsed.append(data_dict)
            except Exception as e:
                print(e)

        # appends as dataframe
        df_data_fills = pd.DataFrame()
        for dict_data in data_parsed:
            # sample data -> can have multiple fills
            # {
            #     "retCode": 0,
            #     "retMsg": "OK",
            #     "result": {
            #         "nextPageCursor": "3154855%3A0%2C3154855%3A0",
            #         "category": "spot",
            #         "list": [
            #             {
            #                 "symbol": "BTCUSDT",
            #                 "orderType": "Market",
            #                 "underlyingPrice": "",
            #                 "orderLinkId": "test_1719821211",
            #                 "orderId": "1720379445568867328",
            #                 "stopOrderType": "",
            #                 "execTime": "1719821211464",
            #                 "feeCurrency": "USDT",
            #                 "feeRate": "0.00015",
            #                 "tradeIv": "",
            #                 "blockTradeId": "",
            #                 "markPrice": "",
            #                 "execPrice": "63311.9",
            #                 "markIv": "",
            #                 "orderQty": "0.000023",
            #                 "orderPrice": "61412.55",
            #                 "execValue": "1.3928618",
            #                 "closedSize": "",
            #                 "execType": "Trade",
            #                 "seq": 33083036412,
            #                 "side": "Sell",
            #                 "indexPrice": "",
            #                 "leavesQty": "0.000001",
            #                 "isMaker": False,
            #                 "execFee": "0.00020892927",
            #                 "execId": "2290000000234990741",
            #                 "marketUnit": "quoteCoin",
            #                 "execQty": "0.000022",
            #             }
            #         ],
            #     },
            #     "retExtInfo": {},
            #     "time": 1719821212110,
            # }
            try:
                fills = dict_data["data"]

                # get fills
                df_data = pd.DataFrame(fills)
                df_data_fills = pd.concat([df_data_fills, df_data])

            except Exception as e:
                continue

        # final adjustments
        # df_data_fills["datetime"] = pd.to_datetime(df_data_fills["execTime"], unit="ms")
        # df_data_fills["execPrice"] = df_data_fills["execPrice"].astype("float")
        # df_data_fills["execQty"] = df_data_fills["execQty"].astype("float")
        # df_data_fills["volume"] = df_data_fills["execPrice"] * df_data_fills["execQty"]
        # df_data_fills.reset_index(drop=True, inplace=True)
        return df_data_fills


if __name__ == "__main__":
    path = os.path.realpath(__file__)
    file_path = os.path.dirname(path) + "/log_files/"
    file_name = "testing.log"
    save_mode = "a"

    # client = LoggerHelper(file_path, file_name, save_mode)
    # client.logger.info("testing")

    # df_binance = LoggerHelper.parse_binance_trade_logs(file_path + "log_binance.log")
    # df_bybit = LoggerHelper.parse_bybit_trade_logs(file_path + "log_bybit.log")
    # df_okx = LoggerHelper.parse_okx_trade_logs(file_path + "log_okx.log")
    # print(df_okx)
