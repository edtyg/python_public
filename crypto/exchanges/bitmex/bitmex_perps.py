import requests
import pandas as pd
import datetime as dt
import math


def get_historical_perps(pair, start_time, end_time):
    
    df = pd.DataFrame()
    diff = end_time - start_time
    call_max = 500 * 3600 * 8 * 1000 # 1000 rows * 3600 seconds * 8 hrs * 1000 (milliseconds)
    
    start_iteration = start_time
    end_iteration = start_time + call_max
    
    if diff <= call_max: # start_time & end_time selected < 1000 rows of data
        start_time_str = dt.datetime.fromtimestamp(start_time/1000).strftime('%Y-%m-%d') #convert epoch time to string
        end_time_str = dt.datetime.fromtimestamp(end_time/1000).strftime('%Y-%m-%d') #convert epoch time to string
        url = f'https://www.bitmex.com/api/v1/funding?symbol={pair}&count=500&reverse=false&startTime={start_time_str}&endTime={end_time_str}' # max 500 rows per call
        response = requests.request("GET", url, headers={}, data={})
        data = response.json()
        df = df.append(data)
    
    elif diff > call_max: # start_time and end_time selected > 1000 rows of data
        num_iterations = math.ceil(diff/call_max) # number of loops required
        for i in range(num_iterations):
            start_time_str = dt.datetime.fromtimestamp(start_iteration/1000).strftime('%Y-%m-%d') #convert epoch time to string
            end_time_str = dt.datetime.fromtimestamp(end_iteration/1000).strftime('%Y-%m-%d') #convert epoch time to string
            url = f'https://www.bitmex.com/api/v1/funding?symbol={pair}&count=500&reverse=false&startTime={start_time_str}&endTime={end_time_str}' # max 1000 rows per call
            response = requests.request("GET", url, headers={}, data={})
            data = response.json()
            df = df.append(data)
            
            start_iteration = end_iteration
            end_iteration = start_iteration + call_max
            
    df['timestamp'] =  pd.to_datetime(df['timestamp'], format= '%Y-%m-%dT%H:%M:%S') #set date format
    df['timestamp'] = df['timestamp'].dt.tz_localize(None)
    df['fundingInterval'] =  pd.to_datetime(df['fundingInterval'], format= '%Y-%m-%dT%H:%M:%S') #set date format
    df['interval'] = df['fundingInterval'].dt.hour

    df.loc[df['interval'] == 0 ,'multiplier'] = 1*365
    df.loc[df['interval'] == 8 ,'multiplier'] = 3*365
    
    df['apy'] = df['fundingRate'] * df['multiplier']
    df['type'] = 'bitmex_coinm_inverse'
    df['exchange'] = 'bitmex'
    
    df = df[['timestamp', 'symbol', 'fundingRate', 'apy', 'type', 'exchange']]
    df.rename(columns={'timestamp':'date'}, inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    return(df)

if __name__ == "__main__":
    save_path = "C:/Users/edgar tan/desktop/python outputs/" #file path
    filename = "bitmex_perps.xlsx" #filename
    
    start_time = int(dt.datetime(2017,1,1,0,0,0).timestamp()*1000) # end time * 1000 > milliseconds
    end_time = int(dt.datetime(2022,1,1,12,0,0).timestamp()*1000) # end time * 1000 > milliseconds
    
    df = get_historical_perps('ETHUSD', start_time, end_time)
    
    writer = pd.ExcelWriter(save_path + filename)
    df.to_excel(writer, sheet_name = 'Funding Rates Combined')
    writer.save()