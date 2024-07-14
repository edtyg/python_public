"""
Bybit Account info - check if it's UTA
"""

from crypto.exchanges.bybit.rest_apis.accounts import spot_client_trade


def setting_margin_mode(client):
    """
    Check on fees

    Args:
        client (_type_): bybit spot client
    """
    mode_setting = client.post_set_margin_mode({"setMarginMode": "PORTFOLIO_MARGIN"})
    return mode_setting


if __name__ == "__main__":

    acc = setting_margin_mode(spot_client_trade)
    print(acc)
