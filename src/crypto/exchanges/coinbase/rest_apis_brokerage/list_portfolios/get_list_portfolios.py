"""
Coinbase Brokerage - derivs acc
"""

from keys.api_personal.crypto_exchanges.coinbase import COINBASE_BROKERAGE_READ
from src.crypto.exchanges.coinbase.rest.coinbase_brokerage_client import (
    CoinbaseBrokerage,
)


def get_portfolio(client):
    """
    Gets Portfolios

    Args:
        client (_type_): coinbase brokerage spot client
    """
    portfolios = client.get_list_portfolios()
    return portfolios


def get_portfolio_breakdwn(client):
    """
    Gets Portfolio breakdown

    Args:
        client (_type_): coinbase brokerage spot client
    """
    portfolios = client.get_portfolio_breakdown("8c618da3-b4e9-529c-9b8a-7f3a8bc6c067")
    return portfolios


if __name__ == "__main__":
    account = COINBASE_BROKERAGE_READ
    coinbase_client = CoinbaseBrokerage(
        account["api_key"],
        account["api_secret"],
    )

    df = get_portfolio(coinbase_client)
    print(df)

    # df_breakdwn = get_portfolio_breakdwn(coinbase_client)
    # print(df_breakdwn)
