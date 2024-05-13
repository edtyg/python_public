"""
Isolated Margin Balances
"""

from src.crypto.exchanges.binance.rest_apis.margin.margin_account import (
    imargin_client_read,
)

if __name__ == "__main__":
    df = imargin_client_read.get_max_borrow_amt(
        {
            "asset": "BTC",
        }
    )
    print(df)
