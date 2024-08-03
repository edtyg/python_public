"""consolidates balances and uploads to postgres"""

import datetime as dt
from exchange_wallet_addresses import addresses
from blockchain_client import BlockChain
from ethplorer import EthPlorer
import pandas as pd
from connection_client import SqlAlchemyConnector

from local_credentials.db_credentials import SGTRD3_MARKETDATA_WRITE
from local_credentials.api_key_data import ETHPLORER_KEY

if __name__ == "__main__":
    sql_client = SqlAlchemyConnector(SGTRD3_MARKETDATA_WRITE)
    blockchain_client = BlockChain()
    eth_client = EthPlorer(ETHPLORER_KEY)
    df = pd.DataFrame()

    curr_time = dt.datetime.now()
    start_time = dt.datetime(
        curr_time.year,
        curr_time.month,
        curr_time.day,
        curr_time.hour,
        curr_time.minute,
        0,
    )

    for exchange, address in addresses.items():
        btc_addresses = address["BTC"]
        eth_addresses = address["ETH"]

        for btc_add in btc_addresses:
            btc_balance = blockchain_client.get_balance(btc_add)
            btc_balance["exchange"] = exchange
            df = pd.concat([df, btc_balance])
            print(f"{exchange} BTC address {btc_add}")

        for eth_add in eth_addresses:
            eth_balance = eth_client.get_erc20_balances(eth_add)
            eth_balance["exchange"] = exchange
            df = pd.concat([df, eth_balance])
            print(f"{exchange} ETH address {eth_add}")
    print(df)

    df_selected_cols = df.drop(columns=["wallet_address", "token_address", "decimals"])
    aggregations = {
        "balance": "sum",
        "price": "mean",
        "market_cap": "sum",
    }

    df_grouped = df_selected_cols.groupby(["exchange", "coin"], as_index=False).agg(
        aggregations
    )
    df_grouped["date"] = start_time
    df_grouped.rename(columns={"balance": "final_balance"}, inplace=True)
    print(df_grouped)

    df_grouped.to_sql("exchange_por", sql_client.engine, if_exists="append")
    print("data appended")
