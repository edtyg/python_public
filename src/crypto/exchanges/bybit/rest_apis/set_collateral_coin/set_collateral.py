"""
Bybit Account info - check if it's UTA
"""

from crypto.exchanges.bybit.rest_apis.accounts import spot_client_trade


def set_collateral_coin(client):
    """
    Check on collateral settings

    Args:
        client (_type_): bybit spot client
    """
    set_coin = client.post_set_collateral_coin(
        {
            "coin": "USDT",
            "collateralSwitch": "ON",
        }
    )
    return set_coin


if __name__ == "__main__":

    coll = set_collateral_coin(spot_client_trade)
    print(coll)
