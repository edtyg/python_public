from crypto.platforms.ftx.rest.ftx_rest_client import FtxClient
from crypto.platforms.ftx.rest.keys import *

import pandas as pd
import datetime as dt
import time

class ftx_rest_data(FtxClient):
    
    def __init__(self, api_key = None, api_secret = None, subaccount_name = None):
        super().__init__(api_key, api_secret, subaccount_name)
    
    def get_perp_spreads(self):
        
        markets = self.get_markets() # get all markets - tradable tickers
        funding = self.get_funding_rates() # get perp funding rates
        borrows = self.get_borrow_rates() # get spot margin borrow rates
        
        df_markets = pd.DataFrame(markets)
        df_funding = pd.DataFrame(funding)
        df_borrows = pd.DataFrame(borrows)
        
        # filter some columns
        df_markets = df_markets[['name', 'price', 'type', 'futureType', 'baseCurrency', 'quoteCurrency', 'underlying', 'volumeUsd24h']]
        
        # spot markets
        df_markets_spot = df_markets.loc[df_markets['type'] == "spot"]
        df_markets_spot = df_markets_spot.loc[df_markets_spot['quoteCurrency'] == 'USD']
        
        # perp markets
        df_markets_perps = df_markets.loc[df_markets['futureType'] == "perpetual"]
        
        # select latest funding rates
        df_funding = df_funding.loc[df_funding['time'] == max(df_funding['time'])]
        
        # adding columns
        for i in df_markets_perps.index:
            underlying = df_markets_perps.loc[i, 'underlying']
            try:
                df_markets_perps.loc[i, 'spot'] = df_markets_spot.loc[df_markets_spot['baseCurrency'] == underlying, 'name'].tolist()[0]
                df_markets_perps.loc[i, 'spot_price'] = df_markets_spot.loc[df_markets_spot['baseCurrency'] == underlying, 'price'].tolist()[0]
                df_markets_perps.loc[i, '24hr_vol_usd'] = df_markets_spot.loc[df_markets_spot['baseCurrency'] == underlying, 'volumeUsd24h'].tolist()[0]
            except:
                df_markets_perps.loc[i, 'spot'] = None
                df_markets_perps.loc[i, 'spot_price'] = None
                df_markets_perps.loc[i, '24hr_vol_usd'] = None
            
        # adding funding rates
        for i in df_markets_perps.index:
            perp_name = df_markets_perps.loc[i, 'name']
            df_markets_perps.loc[i, 'funding_rates'] = df_funding.loc[df_funding['future'] == perp_name, 'rate'].tolist()[0]
        
        # adding spot borrow rates
        for i in df_markets_perps.index:
            try:
                spot_name = df_markets_perps.loc[i, 'underlying']
                df_markets_perps.loc[i, 'spot_borrow_rates'] = df_borrows.loc[df_borrows['coin'] == spot_name, 'estimate'].tolist()[0]
            except:
                next
        
        df_markets_perps = df_markets_perps.dropna(subset = ['spot_borrow_rates', 'spot'])
        
        df_markets_perps['funding_rates_a'] =  df_markets_perps['funding_rates'] * 24 * 365
        df_markets_perps['spot_borrow_rates_a'] =  df_markets_perps['spot_borrow_rates'] * 24 * 365
        
        for i in df_markets_perps.index:
            if df_markets_perps.loc[i, 'funding_rates_a'] > 0:
                df_markets_perps.loc[i, 'spread_margins'] = df_markets_perps.loc[i, 'funding_rates_a']
            else:
                df_markets_perps.loc[i, 'spread_margins'] = abs(df_markets_perps.loc[i, 'funding_rates_a']) - df_markets_perps.loc[i, 'spot_borrow_rates_a']

            
        df_markets_perps = df_markets_perps[['name', 'price', 'volumeUsd24h', 'spot', 'spot_price', '24hr_vol_usd', 'funding_rates_a', 'spot_borrow_rates_a', \
                                             'spread_margins']]
        
        return df_markets_perps
        
        
    def get_all_orders(self, start_time: float):
        # returns all orders from your start time
        
        data = self.get_order_history() # 100 rows each call
        first_df = pd.DataFrame(data)
        timestring = first_df['createdAt'].tolist()[-1] # returns time of earliest order
        timestamp = dt.datetime.strptime(timestring, '%Y-%m-%dT%H:%M:%S.%f+00:00').timestamp()
        
        if start_time >= timestamp:
            return(first_df) # if start time later than earliest order return the latest 100 rows
        
        while start_time <= timestamp:
            data = self.get_order_history(end_time = timestamp) # returns orders before end_time, this returns the next 100 rows
            df = pd.DataFrame(data)

            if df.empty:
                return(first_df)
            timestring = df['createdAt'].tolist()[-1]
            timestamp_new = dt.datetime.strptime(timestring, '%Y-%m-%dT%H:%M:%S.%f+00:00').timestamp()

            first_df = pd.concat([first_df, df])
            timestamp = timestamp_new
            time.sleep(1)
        
        first_df.drop_duplicates(inplace=True)
        first_df.reset_index(drop=True, inplace=True)
        
        return(first_df)
    
    def get_all_fills(self, start_time: float):
        # returns all orders from your start time
        
        data = self.get_fills() # 100 rows each call
        first_df = pd.DataFrame(data)
        timestring = first_df['time'].tolist()[-1] # returns time of earliest order
        timestamp = dt.datetime.strptime(timestring, '%Y-%m-%dT%H:%M:%S.%f+00:00').timestamp()
        
        if start_time >= timestamp:
            return(first_df) # if start time later than earliest order return the latest 100 rows
        
        while start_time <= timestamp:
            data = self.get_fills(end_time = timestamp) # returns orders before end_time, this returns the next 100 rows
            df = pd.DataFrame(data)
            
            if df.empty:
                return(first_df)
            timestring = df['time'].tolist()[-1]
            timestamp_new = dt.datetime.strptime(timestring, '%Y-%m-%dT%H:%M:%S.%f+00:00').timestamp()

            first_df = pd.concat([first_df, df])
            timestamp = timestamp_new
            time.sleep(1)
            
        first_df.drop_duplicates(inplace=True)
        first_df.reset_index(drop=True, inplace=True)
        
        return(first_df)
    
    def get_perp_funding_rates(self, perp_symbol: str, start_time: float):
        # returns all orders from your start time
        
        data = self.get_funding_rates(future = perp_symbol) # 100 rows each call
        first_df = pd.DataFrame(data)
        timestring = first_df['time'].tolist()[-1] # returns time of earliest order
        timestamp = dt.datetime.strptime(timestring, '%Y-%m-%dT%H:%M:%S+00:00').timestamp()
        
        if start_time >= timestamp:
            return(first_df) # if start time later than earliest order return the latest 100 rows
        
        while start_time <= timestamp:
            data = self.get_funding_rates(future = perp_symbol, end_time = timestamp) # returns orders before end_time, this returns the next 100 rows
            df = pd.DataFrame(data)
            
            if df.empty:
                return(first_df)
            timestring = df['time'].tolist()[-1]
            timestamp_new = dt.datetime.strptime(timestring, '%Y-%m-%dT%H:%M:%S+00:00').timestamp()

            first_df = pd.concat([first_df, df])
            timestamp = timestamp_new
            time.sleep(1)
            
        first_df.drop_duplicates(inplace=True)
        first_df.reset_index(drop=True, inplace=True)
        
        return(first_df)
    
    def get_prices(self, market: str, resolution: float, start_time: float):
        # returns all orders from your start time
        
        data = self.get_historical_prices(market = market, resolution = resolution) # 100 rows each call
        first_df = pd.DataFrame(data)
        timestring = first_df['startTime'].tolist()[-1] # returns time of earliest order
        timestamp = dt.datetime.strptime(timestring, '%Y-%m-%dT%H:%M:%S+00:00').timestamp()
        
        if start_time >= timestamp:
            return(first_df) # if start time later than earliest order return the latest 100 rows
        
        while start_time <= timestamp:
            data = self.get_historical_prices(market = market, resolution = resolution, end_time = timestamp) # returns orders before end_time, this returns the next 100 rows
            df = pd.DataFrame(data)
            
            if df.empty:
                return(first_df)
            timestring = df['startTime'].tolist()[-1]
            timestamp_new = dt.datetime.strptime(timestring, '%Y-%m-%dT%H:%M:%S+00:00').timestamp()

            first_df = pd.concat([first_df, df])
            timestamp = timestamp_new
            time.sleep(1)
        
        first_df.sort_values(by = ['startTime'], inplace=True)
        first_df.drop_duplicates(inplace=True)
        first_df.reset_index(drop=True, inplace=True)
        
        return(first_df)
    
if __name__ == "__main__":
    client = ftx_rest_data(ed_api_key, ed_api_secret)
    timestamp = dt.datetime(2022, 11, 1, 1, 0, 0).timestamp()
    
    # spreads = client.get_spreads()
    # orders = client.get_all_orders(timestamp)
    # fills = client.get_all_fills(timestamp)
    # perp_funding = client.get_perp_funding_rates(perp_symbol = 'BTC-PERP', start_time = timestamp)
    prices = client.get_prices(market = 'BTC/USD', resolution = 3600, start_time = timestamp)