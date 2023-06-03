"""
placing spot orders here
"""
from binance_spot import BinanceSpot
from local_credentials.api_key_exchanges import BINANCE_KEY, BINANCE_SECRET

if __name__ == "__main__":
    client = BinanceSpot(BINANCE_KEY, BINANCE_SECRET)

    # order_params = {
    #     "symbol": "ETHBUSD",
    #     "side": "BUY",
    #     "type": "LIMIT",
    #     "timeInForce": "GTC",
    #     "quantity": 1,
    #     "price": 1206,
    # }
    # order1 = client.post_new_order(order_params)
    # order1_id = order1["orderId"]

    # order1_status = client.get_query_order({'symbol': order_params['symbol'], 'orderId': order1_id})
    # order1_cancel = client.delete_cancel_order({'symbol': order_params['symbol'], 'orderId': order1_id})

    # client.get_current_open_orders()
