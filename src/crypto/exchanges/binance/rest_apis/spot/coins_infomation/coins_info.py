"""
Gets Coin information
"""

import pandas as pd

from src.crypto.exchanges.binance.rest_apis.spot.spot_account import spot_client_read


def get_exchange_info(client):
    """
    Gets tick size, step size
    """
    exc_info = client.get_exchange_information({"symbol": "BTCUSDT"})
    return exc_info


def get_coin_info(client):
    """
    coin info
    """
    coin_info = client.get_all_coins_information()
    df_coin_info = pd.DataFrame(coin_info)
    return df_coin_info


if __name__ == "__main__":

    exc_info = get_exchange_info(spot_client_read)
    print(exc_info)

    coin_info = get_coin_info(spot_client_read)
    print(coin_info)
