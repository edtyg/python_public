import requests
import datetime as dt
import pandas as pd
import math
import time

def coin_candles(symbol: str, interval: str, start_time: int, end_time: int):
    """ pulling price data from binance
    maximum of 1000 rows of data per request
    
    Args:
        symbol (str): spot ticker i.e 'BTCBUSD'
        interval (str): '1h'
        start_time (int): timestamp in milliseconds
        end_time (int): timestamp in milliseconds
    """
    
    df = pd.DataFrame()
    time_range = end_time - start_time           # total time range
    request_max = 1000 * 3600 * 1000        # 1000 rows, 3600 seconds * 1000 milliseconds
    
    start_iteration = start_time
    end_iteration = start_time + request_max
    
    base_url = 'https://api.binance.com'
    endpoint = '/api/v3/klines'
    url = base_url + endpoint
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': start_time,
        'endTime': end_time,
        'limit': 1000, # max rows per call = 1000
        }
    
    response_columns = [
        'kline_open_time',
        'open',
        'high',
        'low',
        'close',
        'vol',
        'close_time',
        'quote_vol',
        'num_trades',
        'taker_buy_base_vol',
        'taker_buy_quote_vol',
        'unused_field',
        ]
    
    if time_range <= request_max: # time range selected within 1000 rows limit
        resp = requests.get(url = url, params = params)
        data = resp.json()
        df_data = pd.DataFrame(data, columns = response_columns)
        print(df_data)
        df = pd.concat([df, df_data])
        time.sleep(1)
    
    elif time_range > request_max: # start_time and end_time selected > 1000 rows of data
        num_iterations = math.ceil(time_range/request_max) # number of loops required
        
        for i in range(num_iterations):
            
            resp = requests.get(url = url, params = params)
            data = resp.json()
            df_data = pd.DataFrame(data, columns = response_columns)
            print(df_data)
            df = pd.concat([df, df_data])

                
            start_iteration = end_iteration
            end_iteration = start_iteration + request_max
            params['startTime'], params['endTime'] = start_iteration, end_iteration # adjust params
            time.sleep(1)
            
    df['datetime'] = pd.to_datetime(df['kline_open_time'], unit='ms')
    df.reset_index(drop=True, inplace=True)
    
    return(df)


if __name__ == "__main__":

    start_time = int(dt.datetime(2022, 1, 1, 0, 0, 0).timestamp()*1000) # start time
    end_time = int(dt.datetime(2022, 12, 31, 12, 0, 0).timestamp()*1000) # end time
    print(end_time - start_time)
    
    data = coin_candles('BTCBUSD', '1m', start_time, end_time)
    
    
    
    
    
    
    
    