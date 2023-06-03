import requests
import datetime as dt
import pandas as pd
import math

def deribit_futures_price(symbol, start_time, end_time):
    
    df = pd.DataFrame()
    diff = end_time - start_time
    call_max = 1000 * 3600 * 1000 #744 rows * 3600 seconds * 1000 (milliseconds)
    
    start_iteration = start_time
    end_iteration = start_time + call_max
    
    if diff <= call_max: # start_time & end_time selected < 1000 rows of data    
        url = f'https://www.deribit.com/api/v2/public/get_tradingview_chart_data?end_timestamp={end_time}&instrument_name={symbol}&resolution=60&start_timestamp={start_time}'
        response = requests.request("GET", url, headers={}, data={})
        data = response.json()['result']
        df_temp = pd.DataFrame(data)
        df = df.append(df_temp)
    
    elif diff > call_max: # start_time and end_time selected > 1000 rows of data
        num_iterations = math.ceil(diff/call_max) # number of loops required
        for i in range(num_iterations):
            url = f'https://www.deribit.com/api/v2/public/get_tradingview_chart_data?end_timestamp={end_iteration}&instrument_name={symbol}&resolution=60&start_timestamp={start_iteration}'
            response = requests.request("GET", url, headers={}, data={})
            data = response.json()['result']
            df_temp = pd.DataFrame(data)
            df = df.append(df_temp)
            
            start_iteration = end_iteration
            end_iteration = start_iteration + call_max
            
    df['date'] = pd.to_datetime(df['ticks'], unit='ms') #miliseconds
    df = df[['date', 'close']]
    df['symbol'] = symbol
    df['exchange'] = 'deribit'
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    return(df)

def export_excel(list_of_pairs):
    writer = pd.ExcelWriter(save_path + filename)
    for i in list_of_pairs:
        df = deribit_futures_price(i, start_time, end_time)
        df.to_excel(writer, sheet_name = i)
    
    writer.save()
    print('file Saved')

if __name__ == "__main__":
    save_path = 'C:/Users/edgar tan/Desktop/python outputs/' #edit
    filename = 'deribit_futures_price.xlsx' #edit
    
    start_time = int(dt.datetime(2020,1,1,12,0,0).timestamp()*1000) # start time
    end_time = int(dt.datetime(2021,6,1,12,0,0).timestamp()*1000) # end time
    symbols = ['BTC-PERPETUAL', 'BTC-25JUN21']
    export_excel(symbols)
    
