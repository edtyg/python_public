"""
FalconX api
pip install falconx
"""
import falconx
from local_credentials.api_key_brokers import (
    FALCONX_KEY,
    FALCONX_SECRET,
    FALCONX_PASSPHRASE,
)

if __name__ == "__main__":
    client = falconx.FalconxClient(
        key=FALCONX_KEY, secret=FALCONX_SECRET, passphrase=FALCONX_PASSPHRASE
    )

    balance = client.get_balances()  # current balances
    print(balance)
