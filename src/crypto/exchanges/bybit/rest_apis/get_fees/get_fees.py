"""
Bybit fees
"""

import pandas as pd

from crypto.exchanges.bybit.rest_apis.accounts import spot_client_read


def get_fees(client):
    """
    Check on fees

    Args:
        client (_type_): bybit spot client
    """
    fee = client.get_fee_rate(
        {
            "category": "spot",
            # "symbol": "ETHUSDT",
        }
    )
    df_fee = pd.DataFrame(fee["result"]["list"])
    return df_fee


def vip_data(client):
    """
    Check on vip data

    Args:
        client (_type_): bybit spot client
    """
    fee = client.get_vip_margin_data({"currency": "USDT"})
    return fee


def api_key_info(client):
    """
    Check on vip data

    Args:
        client (_type_): bybit spot client
    """
    key_info = client.get_api_key_info()
    return key_info


if __name__ == "__main__":
    # fees = get_fees(spot_client_read)
    # print(fees)

    # vip_data = vip_data(spot_client_read)
    # print(vip_data)

    keyinfo = api_key_info(spot_client_read)
    print(keyinfo)
