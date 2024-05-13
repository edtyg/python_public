"""
SPOT execution program
"""

from src.crypto.exchanges.binance.rest_apis.margin.margin_account import (
    xmargin_client_read,
)


def retrieve_margin_flows(client):
    """gets transfers etc..."""
    data = client.get_capital_flow(
        {
            "symbol": "BTCUSDT",
            "type": "SELL_INCOME",
        },
    )
    return data


if __name__ == "__main__":

    flows = retrieve_margin_flows(xmargin_client_read)
    print(flows)
