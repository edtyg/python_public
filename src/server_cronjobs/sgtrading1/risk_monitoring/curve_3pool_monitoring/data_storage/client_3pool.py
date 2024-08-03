"""
pip install web3
using web3 library
https://web3py.readthedocs.io/en/stable/quickstart.html#installation

curve 3pool monitoring
https://curve.fi/#/ethereum/pools/3pool/deposit
"""

import datetime as dt

import pandas as pd
from web3 import Web3

from local_credentials.db_credentials import SGTRD3_MARKETDATA_WRITE
from python.sg1_server.cronjobs.risk_monitoring.curve_3pool_monitoring.data_storage.abi import (
    ABI,
)
from python.sg1_server.cronjobs.risk_monitoring.curve_3pool_monitoring.data_storage.connection_client import (
    SqlAlchemyConnector,
)


# 连接到以太坊网络
def main():
    """pulling curve 3pool ratio and saving into sg local postgres database"""
    w3 = Web3(
        Web3.HTTPProvider(
            "https://mainnet.infura.io/v3/d4875f943a104997987982e9835ec449"
        )
    )
    address = "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7"
    contract = w3.eth.contract(address=address, abi=ABI)
    dai_address = ("0x6b175474e89094c44da98b954eedeac495271d0f",)  # dai
    usdc_address = ("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",)  # usdc
    usdt_address = ("0xdac17f958d2ee523a2206206994597c13d831ec7",)  # usdt,
    six_dig_list = [usdc_address, usdt_address]

    def to_decimal(token_amount, address):
        if address in six_dig_list:
            div = 1e6
        else:
            div = 1e18
        return token_amount / div

    dai_token = to_decimal(contract.functions.balances(0).call(), dai_address)
    usdc_token = to_decimal(contract.functions.balances(1).call(), usdc_address)
    usdt_token = to_decimal(contract.functions.balances(2).call(), usdt_address)

    totalSupply = dai_token + usdc_token + usdt_token
    pct_dai = dai_token / totalSupply
    pct_usdc = usdc_token / totalSupply
    pct_usdt = usdt_token / totalSupply

    # print(
    #     "DAI proportion: %.2f \nUSDC proportion: %.2f \nUSDT proportion: %.2f"
    #     % (pct_dai, pct_usdc, pct_usdt)
    # )

    df_3pool = pd.DataFrame(
        data={
            "dai_proportion": pct_dai,
            "usdc_proportion": pct_usdc,
            "usdt_proportion": pct_usdt,
            "dai_supply": dai_token,
            "usdc_supply": usdc_token,
            "usdt_supply": usdt_token,
        },
        index=[dt.datetime.now()],
    )
    print(df_3pool)

    sql_client = SqlAlchemyConnector(SGTRD3_MARKETDATA_WRITE)
    df_3pool.to_sql("curve_3pool_monitor", sql_client.engine, if_exists="append")
    print("data uploaded")


if __name__ == "__main__":
    main()
