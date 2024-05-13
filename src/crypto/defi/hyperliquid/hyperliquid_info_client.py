"""
using hyperliquid python library
pip install hyperliquid-python-sdk
https://github.com/hyperliquid-dex/hyperliquid-python-sdk

use info class for info endpoints - only require wallet address
use exchange class for exchange endpoints - for placing orders
"""

import pandas as pd
from hyperliquid.info import Info
from hyperliquid.utils import constants


def get_user_state(client, wallet: str):
    """
    See a user's open positions and margin summary

    Args:
        client (_type_): info class - from api library
        wallet (str): wallet public address
    """
    user_state = client.user_state(wallet)
    print(user_state)
    return user_state


def get_open_orders(client, wallet: str):
    """
    See a user's open orders

    Args:
        client (_type_): info class - from api library
        wallet (str): wallet public address
    """
    open_orders = client.open_orders(wallet)
    df_open_orders = pd.DataFrame(open_orders)
    df_open_orders["datetime"] = pd.to_datetime(df_open_orders["timestamp"], unit="ms")
    return df_open_orders


def get_user_fills(client, wallet: str):
    """
    Retrieve a user's fills

    Args:
        client (_type_): info class - from api library
        wallet (str): wallet public address
    """
    fills = client.user_fills(wallet)
    df_fills = pd.DataFrame(fills)
    df_fills["datetime"] = pd.to_datetime(df_fills["time"], unit="ms")
    return df_fills


if __name__ == "__main__":
    info_client = Info(constants.MAINNET_API_URL, skip_ws=True)
    wallet_address = "0x52Fb865dbaa7DF26ECC8525560Dd1ab2e683c14c"

    # user_state = get_user_state(info_client, wallet_address)

    # df_open_orders = get_open_orders(info_client, wallet_address)
    # print(df_open_orders)

    # df_fills = get_user_fills(info_client, wallet_address)
    # print(df_fills)
