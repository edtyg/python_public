"""
SPOT execution program
"""

from keys.api_personal.crypto_exchanges.binance import BINANCE_READ, BINANCE_TRADE
from src.crypto.exchanges.binance.rest.binance_isolated_margin import (
    BinanceIsolatedMargin,
)


def get_api_key_permissions(client):
    """Gets current api key permissions"""
    perm = client.get_api_key_permission()
    return perm


def post_transfers(client):
    """Gets cross margin account balances

    type:

    MAIN_MARGIN - Spot account transfer to Margin（cross）account
    MARGIN_MAIN - Margin（cross）account transfer to Spot account

    MAIN_ISOLATED_MARGIN Spot account transfer to Isolated margin account
    ISOLATED_MARGIN_MAIN Isolated margin account transfer to Spot account

    MAIN_UMFUTURE Spot account transfer to USDⓈ-M Futures account
    UMFUTURE_MAIN USDⓈ-M Futures account transfer to Spot account
    """
    transfer = client.post_universal_transfer(
        {
            "type": "MAIN_ISOLATED_MARGIN",
            "asset": "USDT",
            "amount": 1,
            # "fromSymbol": "BTCUSDT",
            "toSymbol": "SOLUSDT",
        }
    )
    return transfer


if __name__ == "__main__":
    api = BINANCE_TRADE
    binance_cross_margin_client = BinanceIsolatedMargin(
        api["api_key"],
        api["api_secret"],
    )

    # set up in both cross and isolated margin client library

    # perm = get_api_key_permissions(binance_cross_margin_client)
    # print(perm)

    # initiate_transfer = post_transfers(binance_cross_margin_client)
    # print(initiate_transfer)
