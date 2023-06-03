from crypto.platforms.ftx.rest.ftx_rest_client import FtxClient
from crypto.platforms.ftx.rest.keys import *

import time
import threading

class ftx_rest_trading(FtxClient):
    
    def __init__(self, api_key: str, api_secret: str, subaccount_name: str = None):
        super().__init__(api_key, api_secret, subaccount_name)
    
    ############################
    ### derived methods here ###
    ############################
    
    def check_balances_positions(self, symbol: str):
        """ Returns balances of base ccy if symbol is spot and futures positions if symbol is a futures symbol

        Args:
            symbol (str): 
                takes in trading symbols like 'ETH/USD', 'ETH-PERP'. 
                Returns the balance of the base currency if spot symbol or futures position if futures symbol -ve value if short (both spot or fut)
        """
        pos = symbol.find('-')
        
        if pos != -1:
            # print('futures symbol')
            # futures symbol
            try:
                fut_position = self.get_positions()
            except:
                time.sleep(0.5)
                fut_position = self.get_positions()
            for fut in fut_position:
                if fut['future'] == symbol:
                    return(fut['size'])
                
        else:
            # print('spot symbol')
            # spot symbol
            backslash_pos = symbol.find('/')
            spot_symbol = symbol[:backslash_pos]
            balances = self.get_balances()
            
            for bal in balances:
                if bal['coin'] == spot_symbol:
                    return(bal['total'])
                
        
    def get_orderbook_prices(self, market: str, side: str) -> float:
        """ Gets prices for top of the orderbook

        Args:
            market (str): TICKER e.g. 'ETH/USD', 'ETH-PERP' etc...
            side (str): 'buy' or 'sell' lowercase

        Returns:
            float: returns the current top of the orderbook price
        """
        if side == 'buy':
            orderbook = self.get_orderbook(market, 1)
            price = orderbook['bids'][0][0] #highest bid price
            
        elif side == 'sell':
            orderbook = self.get_orderbook(market,1)
            price = orderbook['asks'][0][0] #lowest ask price
        
        return price
    
    def post_maker_order(self, market, side, size):
        
        i = 0
        latest_order_id = None
        starting_balance = self.check_balances_positions(market)
        print(f'current balance/positions = {starting_balance}')
        
        if side == 'sell':
            ending_balance = starting_balance - size
            print(f'expected ending balance = {ending_balance}')
        elif side == 'buy':
            ending_balance = starting_balance + size
            print(f'expected ending balance = {ending_balance}')
        
        # places initial order
        initial_price = self.get_orderbook_prices(market, side)
        initial_order = self.place_order(
            market = market,
            side = side,
            price = initial_price,
            size = size,
            type = 'limit',
            post_only = True,
            )

        initial_orderid = initial_order['id']
        latest_order_id = initial_orderid
        initial_order_status = self.get_order_status(initial_orderid)
        remaining_size = initial_order_status['remainingSize']
        print(f'{side} order placed for {market} of size {size}, initial orderid = {initial_orderid}')

        # loop
        while i < 1:
            order_status = self.get_order_status(latest_order_id)
            # print(order_status)
            
            # order placed but non maker order
            if order_status['status'] == 'closed' and order_status['filledSize'] == 0:
                price = self.get_orderbook_prices(market, side)

                # place a new order
                order = self.place_order(
                    market = market,
                    side = side,
                    price = price,
                    size = size,
                    type = 'limit',
                    post_only = True,
                    )
                
                latest_order_id = order['id']
                
                print(f'new {side} order placed for {market} of size {size}, latest orderid = {latest_order_id}')
                time.sleep(1)
            
            # partial filled
            elif order_status['status'] == 'open' and order_status['remainingSize'] != 0:
                price = self.get_orderbook_prices(market, side)
 
                # still top of orderbook
                if price == order_status['price']:
                    print(f'current {side} price still at top of orderbook')
                    time.sleep(1)
                
                # no longer top of the order book
                elif price != order_status['price']:
                    print(f'current {side} price not at top of orderbook')
                    remaining_size = order_status['remainingSize']
                    try:
                        order = self.modify_order(
                            existing_order_id = latest_order_id, 
                            price = price,
                            size = remaining_size,
                            )
                        latest_order_id = order['id']
                        order_status = self.get_order_status(latest_order_id)
                        print(f'{side} order placed for {market} of size {remaining_size}, latest orderid = {latest_order_id}')
                        time.sleep(1)
                    except:
                        next

            # fully filled
            elif order_status['status'] == 'closed' and order_status['filledSize'] == remaining_size:
                i += 1
                print("Order Completed")
                time.sleep(1)
            
            # additional checking of positions
            elif (side == 'sell' and self.check_balances_positions(market) <= ending_balance) or (side == 'buy' and self.check_balances_positions(market) >= ending_balance):
                i += 1
                print("Order Completed")
                time.sleep(1)
    
    def futures_spread(self, buy_market, sell_market, total_size : float, clip_size : float):
        
        number_of_loops = int(total_size/clip_size)
        
        i = 0
        
        while i < int(number_of_loops):
            t1 = threading.Thread(target=self.post_maker_order, args=[buy_market, 'buy', clip_size])
            t2 = threading.Thread(target=self.post_maker_order, args=[sell_market, 'sell', clip_size])
            
            t1.start()
            t2.start()
            
            t1.join()
            t2.join()
            
            print(f'clip {i+1} completed')
            i += 1
    
    
if __name__ == "__main__":
    
    ftx_own = ftx_rest_trading(ed_api_key, ed_api_secret)
    ftx_mum = ftx_rest_trading(mum_api_key, mum_api_secret)
    
    # ftx_own.post_maker_order('BTC-PERP', 'sell', 0.066)
    ftx_own.futures_spread('BTC-PERP', 'BTC/USD', 0.1, 0.1)
    
    
    