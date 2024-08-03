"""
Script to save platform balances into our database

"datetime", "coin", "amount", "type", "account"
"""

import asyncio
import datetime as dt
import os
import time

import independentreserve as ir
import pandas as pd

### api keys ###
from keys.api_work.crypto_brokers.b2c2 import B2C2_HTS_READ
from keys.api_work.crypto_brokers.independent_reserve import IR_HTS_READ
from keys.api_work.crypto_exchanges.binance import BINANCE_MCA_MAIN_READ
from keys.api_work.crypto_exchanges.bybit import (
    BYBIT_MCA_LTP1_READ,
    BYBIT_MCA_MAIN_READ,
)
from keys.api_work.crypto_exchanges.coinbase import (
    COINBASE_BROKERAGE_HTS_READ,
    COINBASE_EXCHANGE_HTS_READ,
)
from keys.api_work.crypto_exchanges.hashkey import HASHKEYEXCHANGE_HTS_MAIN_READ
from keys.api_work.crypto_exchanges.okx import OKX_MCA_LTP1_READ, OKX_MCA_MAIN_READ
from keys.api_work.custody.hextrust_v2 import HEXTRUST_V2
from keys.api_work.databases.postgres import SG_TRADING_3_MARKETDATA_WRITE

### library imports ###
from src.crypto.brokers.b2c2.rest.b2c2_client import B2C2Rest
from src.crypto.custody.hextrust.hextrust_v2_client import hexsafe_v2
from src.crypto.exchanges.binance.rest.binance_cross_margin import BinanceCrossMargin
from src.crypto.exchanges.binance.rest.binance_isolated_margin import (
    BinanceIsolatedMargin,
)
from src.crypto.exchanges.binance.rest.binance_spot import BinanceSpot
from src.crypto.exchanges.bybit.rest.bybit_client import Bybit
from src.crypto.exchanges.coinbase.rest.coinbase_brokerage_client import (
    CoinbaseBrokerage,
)
from src.crypto.exchanges.coinbase.rest.coinbase_exchange_client import CoinbaseExchange
from src.crypto.exchanges.hashkey.rest.hashkey_hk.hashkey_spot_hk import HashkeySpot
from src.crypto.exchanges.okx.rest.okx_client import Okx

### misc imports ###
from src.server_cronjobs.sgtrading1.balance_snaps_finance.misc.logger_client import (
    LoggerClient,
)
from src.server_cronjobs.sgtrading1.balance_snaps_finance.misc.sqlalchemy_client import (
    SqlAlchemyConnector,
)
from src.server_cronjobs.sgtrading1.balance_snaps_finance.safeheron.demo.api_demo.account.account_api_demo import (
    TestAccount,
)

### logger settings ###
full_path = os.path.realpath(__file__)
save_path = os.path.dirname(full_path) + "/"
log_filename = "save_account_balances.log"
log_client = LoggerClient(save_path, log_filename, "a")

### sql database ###
sql_client = SqlAlchemyConnector(SG_TRADING_3_MARKETDATA_WRITE)
sql_client.postgres_connection()


def b2c2_balances():
    """save b2c2 balance"""
    client = B2C2Rest(B2C2_HTS_READ["api_key"])
    mapper = {
        "USC": "USDC",
        "UST": "USDT",
    }
    try:
        bal = client.get_balances()
        df = pd.DataFrame(list(bal.items()), columns=["coin", "amount"])
        df["amount"] = pd.to_numeric(df["amount"])
        df = df.loc[df["amount"] != 0]

        if not df.empty:
            df["type"] = "spot"
            df["account"] = "B2C2_HTS_MAIN"
            df["datetime"] = dt.datetime.now()
            df = df[["datetime", "coin", "amount", "type", "account"]]
            df["coin"] = df["coin"].map(mapper).fillna(df["coin"])
            df.to_sql(
                "account_balances",
                sql_client.engine,
                if_exists="append",
                index=False,
            )
            print("b2c2 balance saved")
            log_client.logger.info("b2c2 balance saved")
        else:
            df = pd.DataFrame()
    except Exception as e:
        print(e)
        log_client.logger.warning(e)
    return df


def binance_balances():
    """save binance balances"""
    df_final = pd.DataFrame()
    try:
        account = {
            "BINANCE_MCA_MAIN": BINANCE_MCA_MAIN_READ,
        }

        for key, value in account.items():
            df_account = pd.DataFrame()
            # clients
            spot_client = BinanceSpot(value["api_key"], value["api_secret"])
            cm_client = BinanceCrossMargin(value["api_key"], value["api_secret"])
            im_client = BinanceIsolatedMargin(value["api_key"], value["api_secret"])

            # pulling spot balances
            spot_balance = spot_client.post_user_asset()
            df_spot_balance = pd.DataFrame(spot_balance)

            if not df_spot_balance.empty:
                df_spot_balance["total"] = (
                    df_spot_balance["free"].astype("float")
                    + df_spot_balance["locked"].astype("float")
                    + df_spot_balance["freeze"].astype("float")
                    + df_spot_balance["withdrawing"].astype("float")
                    + df_spot_balance["ipoable"].astype("float")
                )
                df_spot_balance = df_spot_balance[["asset", "total"]]
                df_spot_balance["type"] = "spot"
                df_spot_balance["account"] = key
                df_spot_balance["datetime"] = dt.datetime.now()
                df_spot_balance = df_spot_balance.rename(
                    columns={"total": "amount", "asset": "coin"}
                )
                df_spot_balance = df_spot_balance[
                    ["datetime", "coin", "amount", "type", "account"]
                ]
            else:
                df_spot_balance = pd.DataFrame()

            # cross_margin_balance
            cross_margin_balance = cm_client.get_cross_margin_details()
            df_cross_margin = pd.DataFrame(cross_margin_balance["userAssets"])
            df_cross_margin["netAsset"] = df_cross_margin["netAsset"].astype("float")
            df_cross_margin = df_cross_margin.loc[df_cross_margin["netAsset"] != 0]

            if not df_cross_margin.empty:
                df_cross_margin["datetime"] = dt.datetime.now()
                df_cross_margin["type"] = "cross_margin"
                df_cross_margin["account"] = key
                df_cross_margin = df_cross_margin.rename(
                    columns={"asset": "coin", "netAsset": "amount"}
                )
                df_cross_margin = df_cross_margin[
                    ["datetime", "coin", "amount", "type", "account"]
                ]
            else:
                df_cross_margin = pd.DataFrame()

            # isolated_margin_balance
            iso_margin = {}
            iso_margin_balance = im_client.get_isolated_margin_info()
            assets = iso_margin_balance["assets"]
            for i in assets:
                base_asset = i["baseAsset"]["asset"]
                base_asset_amt = float(i["baseAsset"]["netAsset"])
                if base_asset not in iso_margin:
                    iso_margin[base_asset] = base_asset_amt
                else:
                    curr_base_amt = iso_margin[base_asset]
                    iso_margin[base_asset] = base_asset_amt + curr_base_amt

                quote_asset = i["quoteAsset"]["asset"]
                quote_asset_amt = float(i["quoteAsset"]["netAsset"])
                if quote_asset not in iso_margin:
                    iso_margin[quote_asset] = quote_asset_amt
                else:
                    curr_quote_amt = iso_margin[quote_asset]
                    iso_margin[quote_asset] = quote_asset_amt + curr_quote_amt

                df_iso_margin = pd.DataFrame(iso_margin, index=[0]).T
                df_iso_margin.reset_index(drop=False, inplace=True)
                df_iso_margin.columns = ["coin", "amount"]
                df_iso_margin["datetime"] = dt.datetime.now()
                df_iso_margin["type"] = "isolated_margin"
                df_iso_margin["account"] = key
                df_iso_margin = df_iso_margin[
                    ["datetime", "coin", "amount", "type", "account"]
                ]

            df_account = pd.concat(
                [df_account, df_spot_balance, df_cross_margin, df_iso_margin]
            )
            df_account.to_sql(
                "account_balances", sql_client.engine, if_exists="append", index=False
            )
            log_client.logger.info(f"{key} balance saved")
            df_final = pd.concat([df_final, df_account])
        return df_final

    except Exception as e:
        print(e)
        log_client.logger.warning(e)


def bybit_balances():
    """save bybit balances"""
    df_final = pd.DataFrame()
    try:
        account = {
            "BYBIT_MCA_MAIN": BYBIT_MCA_MAIN_READ,
            "BYBIT_MCA_LTP1": BYBIT_MCA_LTP1_READ,
        }
        for key, value in account.items():
            df_account = pd.DataFrame()
            client = Bybit(value["api_key"], value["api_secret"])

            funding_balances = client.get_all_coins_balance({"accountType": "FUND"})
            uta_acc = client.get_all_coins_balance({"accountType": "UNIFIED"})

            df_funding_balances = pd.DataFrame(funding_balances["result"]["balance"])
            df_funding_balances["type"] = "funding_account"

            df_uta_balances = pd.DataFrame(uta_acc["result"]["balance"])
            df_uta_balances["type"] = "uta_account"

            df_account = pd.concat(
                [
                    df_funding_balances,
                    df_uta_balances,
                ]
            )

            df_account["walletBalance"] = df_account["walletBalance"].astype("float")
            df_account = df_account.loc[df_account["walletBalance"] > 0]
            df_account["datetime"] = dt.datetime.now()
            df_account["account"] = key
            df_account = df_account[
                ["datetime", "coin", "walletBalance", "type", "account"]
            ]
            df_account.rename(columns={"walletBalance": "amount"}, inplace=True)
            df_account.to_sql(
                "account_balances", sql_client.engine, if_exists="append", index=False
            )
            log_client.logger.info(f"{key} balance saved")
            df_final = pd.concat([df_final, df_account])
        return df_final
    except Exception as e:
        print(e)
        log_client.logger.warning(e)


def coinbase_brokerage_balances():
    """save coinbase brokerage balances"""
    try:
        account = {
            "COINBASE_BROKERAGE_HTS_MAIN": COINBASE_BROKERAGE_HTS_READ,
        }
        for key, value in account.items():
            client = CoinbaseBrokerage(
                value["api_key"],
                value["api_secret"],
            )
            accounts = client.list_accounts()

            data = accounts["accounts"]
            df_spot_balances = pd.DataFrame(data)

            for i in df_spot_balances.index:
                df_spot_balances.loc[i, "amount"] = df_spot_balances.loc[
                    i, "available_balance"
                ]["value"]

            df_spot_balances["datetime"] = dt.datetime.now()
            df_spot_balances["type"] = "coinbase_brokerage"
            df_spot_balances["account"] = key

            df_spot_balances = df_spot_balances.rename(
                columns={
                    "currency": "coin",
                    "balance": "amount",
                }
            )
            df_spot_balances = df_spot_balances[
                ["datetime", "coin", "amount", "type", "account"]
            ]
            df_spot_balances["amount"] = df_spot_balances["amount"].astype("float")
            df_spot_balances = df_spot_balances.loc[df_spot_balances["amount"] != 0]

        df_spot_balances.to_sql(
            "account_balances", sql_client.engine, if_exists="append", index=False
        )
        log_client.logger.info(f"{key} balance saved")
        return df_spot_balances
    except Exception as e:
        print(e)
        log_client.logger.warning(e)


def coinbase_exchange_balances():
    """save coinbase exchange balances"""
    try:
        account = {
            "COINBASE_EXCHANGE_HTS_MAIN": COINBASE_EXCHANGE_HTS_READ,
        }
        for key, value in account.items():
            client = CoinbaseExchange(
                value["api_key"], value["api_secret"], value["passphrase"]
            )

            # funding account balances
            balance = client.get_all_accounts()
            df_balance = pd.DataFrame(balance)
            df_balance["balance"] = df_balance["balance"].astype("float")
            df_balance["datetime"] = dt.datetime.now()
            df_balance["type"] = "coinbase_exchange"
            df_balance["account"] = key

            df_balance = df_balance.rename(
                columns={
                    "currency": "coin",
                    "balance": "amount",
                }
            )
            df_balance = df_balance[["datetime", "coin", "amount", "type", "account"]]
            df_balance = df_balance.loc[df_balance["amount"] != 0]

        df_balance.to_sql(
            "account_balances", sql_client.engine, if_exists="append", index=False
        )
        log_client.logger.info(f"{key} balance saved")
        return df_balance
    except Exception as e:
        print(e)
        log_client.logger.warning(e)


def okx_balances():
    """save okx balances"""
    df_final = pd.DataFrame()
    try:
        account = {
            "OKX_MCA_MAIN": OKX_MCA_MAIN_READ,
            "OKX_MCA_LTP1": OKX_MCA_LTP1_READ,
        }
        for key, value in account.items():
            df_account = pd.DataFrame()
            client = Okx(value["api_key"], value["api_secret"], value["passphrase"])

            # funding account balances
            funding_balance = client.get_balance_funding()
            if funding_balance["data"]:
                df_funding_balance = pd.DataFrame(funding_balance["data"])
                df_funding_balance["datetime"] = dt.datetime.now()
                df_funding_balance["type"] = "funding"
                df_funding_balance["account"] = key
                df_funding_balance = df_funding_balance.rename(
                    columns={"bal": "amount", "ccy": "coin"}
                )
                df_funding_balance = df_funding_balance[
                    ["datetime", "coin", "amount", "type", "account"]
                ]
            else:
                df_funding_balance = pd.DataFrame()

            # trading account balances
            trading_balance = client.get_balance_trading()
            if trading_balance["data"][0]["details"]:
                df_trading_balance = pd.DataFrame(trading_balance["data"][0]["details"])
                df_trading_balance["datetime"] = dt.datetime.now()
                df_trading_balance["type"] = "trading"
                df_trading_balance["account"] = key
                df_trading_balance = df_trading_balance.rename(
                    columns={"eq": "amount", "ccy": "coin"}
                )
                df_trading_balance = df_trading_balance[
                    ["datetime", "coin", "amount", "type", "account"]
                ]
            else:
                df_trading_balance = pd.DataFrame()

            # combined
            log_client.logger.info(f"{key} balance saved")
            df_account = pd.concat([df_funding_balance, df_trading_balance])
            df_final = pd.concat([df_final, df_account])

        df_final.to_sql(
            "account_balances", sql_client.engine, if_exists="append", index=False
        )
        print("okx balance saved")
        return df_final
    except Exception as e:
        print(e)
        log_client.logger.warning(e)


def hashkey_exchange_balances():
    """save ir balances"""
    try:
        account = HASHKEYEXCHANGE_HTS_MAIN_READ
        client = HashkeySpot(account["api_key"], account["api_secret"])

        df_final = pd.DataFrame()
        account_dict = {
            "custody_balance": "1468013748774110721",
            "fiat_balance": "1468013748774110722",
            "trading_balance": "1468013748774110720",
            "opt_balance": "1468177790721468160",
        }

        for key, value in account_dict.items():
            balance = client.get_account_info({"accountId": value})
            df_balance = pd.DataFrame(balance["balances"])
            if df_balance.empty is False:
                df_balance["datetime"] = dt.datetime.now()
                df_balance["type"] = key
                df_balance["account"] = "HASHKEY_EXCHANGE_HTS_MAIN"
                df_balance = df_balance.rename(
                    columns={"total": "amount", "asset": "coin"}
                )
                df_balance = df_balance[
                    ["datetime", "coin", "amount", "type", "account"]
                ]
                df_final = pd.concat([df_final, df_balance])
            time.sleep(0.3)

        df_final.to_sql(
            "account_balances", sql_client.engine, if_exists="append", index=False
        )
        log_client.logger.info(f"{key} balance saved")
        return df_final
    except Exception as e:
        print(e)
        log_client.logger.warning(e)


def independent_reserve_balances():
    """save independent reserve balances"""
    try:
        account = IR_HTS_READ
        client = ir.PrivateMethods(account["api_key"], account["api_secret"])
        balances = client.get_accounts()
        if balances:
            df_balance = pd.DataFrame(balances)
            df_balance["datetime"] = dt.datetime.now()
            df_balance["type"] = "spot"
            df_balance["account"] = "IR_HTS_MAIN"
            df_balance = df_balance.rename(
                columns={"TotalBalance": "amount", "CurrencyCode": "coin"}
            )
            df_balance = df_balance[["datetime", "coin", "amount", "type", "account"]]
            df_balance["amount"] = df_balance["amount"].astype("float")
            df_balance = df_balance.loc[df_balance["amount"] != 0]
            df_balance.loc[df_balance["coin"] == "Xbt", "coin"] = "BTC"

            df_balance.to_sql(
                "account_balances", sql_client.engine, if_exists="append", index=False
            )
            log_client.logger.info("IR balance saved")
        return df_balance
    except Exception as e:
        print(e)
        log_client.logger.warning(e)


def hextrust_v2_balances():
    """save hextrust v2 balances"""
    account = HEXTRUST_V2
    save_path = os.path.dirname(os.path.realpath(__file__))
    pem_filename = "/my_rsa.pem"
    pem_filepath = save_path + pem_filename

    with open(pem_filepath, "r") as pem_file:
        pem_data = pem_file.read()
    client = hexsafe_v2(pem_data, account["api_key"])

    try:
        balance = client.main()
        balance["datetime"] = dt.datetime.now()
        balance["account"] = "HEXTRUST_HTS_MAIN"

        balance = balance.rename(
            columns={
                "total": "amount",
                "wallet_name": "remarks",
                "mapped_tokens": "coin",
            }
        )
        balance = balance[["datetime", "coin", "amount", "type", "account", "remarks"]]
        balance.to_sql(
            "account_balances", sql_client.engine, if_exists="append", index=False
        )
        log_client.logger.info("HEX V2 balance saved")
        return balance
    except Exception as e:
        print(e)
        log_client.logger.warning(e)


def safeheron_balances():
    """save safeheron balances"""
    df_final = pd.DataFrame()
    client = TestAccount()
    account_id = {
        "Wallet1_Asset": "account3642c2bc2b5b4d4183c7127f58b1ce8a",
        "Wallet2_Asset": "account36670f9775ff4dad88b5246f01d713e5",
    }

    for key, value in account_id.items():
        balances = client.test_list_account_coins(value)

        df_balance = pd.DataFrame(balances)
        df_balance["balance"] = df_balance["balance"].astype("float")
        df_balance = df_balance.loc[df_balance["balance"] > 0]

        if not df_balance.empty:
            df_balance["datetime"] = dt.datetime.now()
            df_balance["type"] = "spot"
            df_balance["account"] = "SAFEHERON_HTS_MAIN"
            df_balance["remarks"] = key
            df_balance = df_balance.rename(
                columns={
                    "coinName": "coin",
                    "balance": "amount",
                    "account_name": "remarks",
                }
            )
            df_balance = df_balance[
                ["datetime", "coin", "amount", "type", "account", "remarks"]
            ]
            df_final = pd.concat([df_final, df_balance])

    df_final.to_sql(
        "account_balances", sql_client.engine, if_exists="append", index=False
    )
    print("safeheron balance saved")
    return df_final


# async def safeheron_web3():
#     """
#     save safeheron web3 wallet balances
#     using ethplorer to pull balances
#     """
#     client = ETHPlorer(ETHPLORER_KEY["api_key"])

#     df_final = pd.DataFrame()
#     for wallet_name, wallet_address in erc_wallet_addresses.items():
#         print(wallet_name, wallet_address)
#         address_info = client.get_address_info(wallet_address)
#         eth_balance = address_info["ETH"]["balance"]
#         data_eth = {
#             "balance": float(eth_balance),
#             "token_address": "NA",
#             "token_decimals": 0,
#             "token_symbol": "ETH",
#             "wallet_name": wallet_name,
#             "wallet_address": wallet_address,
#         }
#         df_data_eth = pd.DataFrame(data_eth, index=[0])
#         df_final = pd.concat([df_final, df_data_eth])

#         try:
#             tokens_list = address_info["tokens"]
#         except:
#             print("no other erc tokens for this address")
#             tokens_list = []

#         if tokens_list:
#             for tokens in tokens_list:
#                 token_balance = float(tokens["balance"])
#                 token_address = tokens["tokenInfo"]["address"]
#                 token_decimals = int(tokens["tokenInfo"]["decimals"])
#                 token_symbol = tokens["tokenInfo"]["symbol"]

#                 data_tokens = {
#                     "balance": token_balance,
#                     "token_address": token_address,
#                     "token_decimals": token_decimals,
#                     "token_symbol": token_symbol,
#                     "wallet_name": wallet_name,
#                     "wallet_address": wallet_address,
#                 }
#                 df_data_tokens = pd.DataFrame(data_tokens, index=[0])
#                 df_final = pd.concat([df_final, df_data_tokens])

#     df_final.reset_index(drop=True, inplace=True)
#     for i in df_final.index:
#         decimal = df_final.loc[i, "token_decimals"]
#         balance = df_final.loc[i, "balance"]
#         multiplier = 1 * 10**decimal
#         adjusted_balance = balance / multiplier
#         df_final.loc[i, "adjusted_balance"] = adjusted_balance

#     df_final["datetime"] = dt.datetime.now()
#     df_final["type"] = "safeheron_web3_wallet"
#     df_final["account"] = "SAFEHERON_HTS_MAIN"

#     df_final = df_final[
#         [
#             "datetime",
#             "token_symbol",
#             "adjusted_balance",
#             "type",
#             "account",
#             "wallet_name",
#         ]
#     ]

#     df_final = df_final.rename(
#         columns={
#             "token_symbol": "coin",
#             "adjusted_balance": "amount",
#             "wallet_name": "remarks",
#         }
#     )
#     print(df_final)

#     df_final.to_sql(
#         "account_balances", sql_client.engine, if_exists="append", index=False
#     )
#     print("safeheron web3 wallet balances saved")


if __name__ == "__main__":
    ### excel file ###
    main_excel_file = save_path + "main.xlsx"

    # excel file
    try:
        df_excel = pd.read_excel(main_excel_file, engine="openpyxl", index_col=0)
    except Exception as e:
        print(e)
        df_excel = pd.DataFrame()

    df_b2c2 = b2c2_balances()
    df_binance = binance_balances()
    df_bybit = bybit_balances()
    df_cb_brokerage = coinbase_brokerage_balances()
    df_cb_exc = coinbase_exchange_balances()
    df_okx = okx_balances()
    df_hkex = hashkey_exchange_balances()
    df_ir = independent_reserve_balances()
    df_hex_v2 = hextrust_v2_balances()
    df_sh = safeheron_balances()
    # safeheron_web3()

    df_excel = pd.concat(
        [
            df_excel,
            df_b2c2,
            df_binance,
            df_bybit,
            df_cb_brokerage,
            df_cb_exc,
            df_okx,
            df_hkex,
            df_ir,
            df_hex_v2,
            df_sh,
        ]
    )
    print(df_excel)
    writer = pd.ExcelWriter(save_path + "main.xlsx")
    df_excel.to_excel(writer, sheet_name="balances")
    writer.close()
    print("excel records saved")
