import requests
import datetime as dt
import pandas as pd
import math

def deribit_perp_funding(symbol, start_time, end_time):
    
    df = pd.DataFrame()
    diff = end_time - start_time
    call_max = 744 * 3600 * 1000 #744 rows * 3600 seconds * 1000 (milliseconds)
    
    start_iteration = start_time
    end_iteration = start_time + call_max
    
    if diff <= call_max: # start_time & end_time selected < 1000 rows of data    
        url = f'https://www.deribit.com/api/v2/public/get_funding_rate_history?end_timestamp={end_time}&start_timestamp={start_time}&instrument_name={symbol}'
        response = requests.request("GET", url, headers={}, data={})
        data = response.json()['result']
        df = df.append(data)
    
    elif diff > call_max: # start_time and end_time selected > 1000 rows of data
        num_iterations = math.ceil(diff/call_max) # number of loops required
        for i in range(num_iterations):
            url = f'https://www.deribit.com/api/v2/public/get_funding_rate_history?end_timestamp={end_iteration}&start_timestamp={start_iteration}&instrument_name={symbol}'
            response = requests.request("GET", url, headers={}, data={})
            data = response.json()['result']
            df = df.append(data)
            
            start_iteration = end_iteration
            end_iteration = start_iteration + call_max
    
    df['symbol'] = symbol
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms') #miliseconds
    df['apy'] = pd.to_numeric(df['interest_1h']) * 24 * 365 # creating apy values, 8hr * 3 times a day * 365 days
    df['type'] = 'deribit_coinm'
    df['exchange'] = 'deribit'
    df = df[['date','symbol','interest_1h','apy','type','exchange']] #rearranging and selecting columns
    df.rename(columns={'interest_1h':'fundingRate'}, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.drop_duplicates(inplace=True)
    return(df)

if __name__ == "__main__":
    save_path = 'C:/Users/edgar tan/Desktop/python outputs/' #edit
    filename = 'deribit_perp_funding.xlsx' #edit
    
    start_time = int(dt.datetime(2021,1,1,12,0,0).timestamp()*1000) # start time
    end_time = int(dt.datetime(2021,6,1,12,0,0).timestamp()*1000) # end time
    
    df = deribit_perp_funding('BTC-PERPETUAL', start_time, end_time)
    
    writer = pd.ExcelWriter(save_path + filename)
    df.to_excel(writer, sheet_name = 'Spot vs Futures')
    writer.save()
    print('file Saved')