import requests
import pandas as pd
import datetime as dt
import math
import time

def bitmex_index(pair, start_time, end_time):
    
    df = pd.DataFrame()
    diff = end_time - start_time
    call_max = 9 * 3600 * 24 * 1000 # 10 rows * 60 seconds * 8 hrs * 1000 (milliseconds)
    
    start_iteration = start_time
    end_iteration = start_time + call_max
    
    num_iterations = math.floor(diff/call_max) # number of loops required
    for i in range(num_iterations):
        start_time_str = dt.datetime.fromtimestamp(start_iteration/1000).strftime('%Y-%m-%d') #convert epoch time to string
        end_time_str = dt.datetime.fromtimestamp(end_iteration/1000).strftime('%Y-%m-%d') #convert epoch time to string
        url = f'https://www.bitmex.com/api/v1/trade?symbol={pair}&count=500&reverse=false&startTime={start_time_str}&endTime={end_time_str}&filter=%7B%22timestamp.time.hh%22%3A%2200%3A00%22%7D'
        time.sleep(1)
        response = requests.request("GET", url, headers={}, data={})
        data = response.json()
        df = df.append(data, ignore_index = True)
        print(df)
        
        start_iteration = end_iteration
        end_iteration = start_iteration + call_max
    
    end_iteration = int(dt.datetime(2017,1,1,0,0,0).now().timestamp()*1000) # set to latest current time
    start_time_str = dt.datetime.fromtimestamp(start_iteration/1000).strftime('%Y-%m-%d') #convert epoch time to string
    end_time_str = dt.datetime.fromtimestamp(end_iteration/1000).strftime('%Y-%m-%d') #convert epoch time to string
    url = f'https://www.bitmex.com/api/v1/trade?symbol={pair}&count=500&reverse=false&startTime={start_time_str}&endTime={end_time_str}&filter=%7B%22timestamp.time.hh%22%3A%2200%3A00%22%7D' 
    time.sleep(1)
    response = requests.request("GET", url, headers={}, data={})
    data = response.json()
    df = df.append(data, ignore_index = True)
    
    df['timestamp'] =  pd.to_datetime(df['timestamp'], format= '%Y-%m-%dT%H:%M:%S') #set date format
    df['timestamp'] = df['timestamp'].dt.tz_localize(None)
    print(df)
    
    df = df[['timestamp', 'symbol', 'price']]
    
    return(df)

if __name__ == "__main__":
    save_path = "C:/Users/edgar tan/desktop/python outputs/" #file path
    filename = "bitmex_perps_index.xlsx" #filename
    
    start_time = int(dt.datetime(2018,7,1,0,0,0).timestamp()*1000) # end time * 1000 > milliseconds  2018 jul eth, 2017 apr btc
    end_time = int(dt.datetime(2021,5,11,12,0,0).timestamp()*1000) # end time * 1000 > milliseconds
    df = bitmex_index('.BETH', start_time, end_time) # .BXBT for btc index .BETH for eth index
    
    writer = pd.ExcelWriter(save_path + filename)
    df.to_excel(writer, sheet_name = 'Funding Rates Combined')
    writer.save()