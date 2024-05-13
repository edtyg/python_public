"""
pip install dydx-v3-python - install lib
"""

import time

from dydx3 import Client

from local_credentials.api_key_defi import (
    DYDX_KEY,
    DYDX_SECRET,
    DYDX_PASSPHRASE,
    STARK_PRIVATE_KEY,
    ETH_WALLET_ADDRESS,
)

if __name__ == "__main__":
    client = Client(
        host="https://api.dydx.exchange",
        default_ethereum_address=ETH_WALLET_ADDRESS,  # your eth wallet address
        stark_private_key=STARK_PRIVATE_KEY,
        api_key_credentials={
            "key": DYDX_KEY,
            "secret": DYDX_SECRET,
            "passphrase": DYDX_PASSPHRASE,
        },
    )

    user = client.private.get_user()
    account = client.private.get_account()
    accounts = client.private.get_accounts()
    all_positions = client.private.get_positions()
    all_fills = client.private.get_fills()
    all_orders = client.private.get_orders()

    # place order here
    # placed_order = client.private.create_order(
    #     position_id = client.private.get_account().data['account']['positionId'], # required for creating the order signature
    #     market = 'ETH-USD',
    #     side = 'BUY',
    #     order_type = 'LIMIT',
    #     post_only = True,
    #     size = '0.01',
    #     price = '1200',
    #     limit_fee = '0.015',
    #     expiration_epoch_seconds = int(time.time() + 60 * 60 * 10),
    #     time_in_force = 'GTT',
    #     )
    # placed_order_id = placed_order.data['order']['id']

    # cancel_order = client.private.cancel_order(order_id = placed_order_id)
