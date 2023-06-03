import requests
import pandas as pd
import datetime as dt
import math

def bitfinex_perp_funding_rates(symbol, start_time, end_time):
    
    df_final = pd.DataFrame()
    diff = end_time - start_time
    call_max = 5000 * 60 * 1000 # 1000 rows * 60 seconds * 8 hrs * 1000 (milliseconds)
    
    col_names = ['MTS',
        'PLACEHOLDER', 
        'DERIV_PRICE',
        'SPOT_PRICE',
        'PLACEHOLDER',
        'INSURANCE_FUND_BALANCE',
        'PLACEHOLDER',
        'NEXT_FUNDING_EVT_TIMESTAMP_MS',
        'NEXT_FUNDING_ACCRUED',
        'NEXT_FUNDING_STEP',
        'PLACEHOLDER',
        'CURRENT_FUNDING',
        'PLACEHOLDER',
        'PLACEHOLDER',
        'MARK_PRICE',
        'PLACEHOLDER',
        'PLACEHOLDER',
        'OPEN_INTEREST',
        'PLACEHOLDER',
        'PLACEHOLDER',
        'PLACEHOLDER',
        'CLAMP_MIN',
        'CLAMP_MAX'
      ]
    
    
    start_iteration = start_time
    end_iteration = start_time + call_max
    
    num_iterations = math.floor(diff/call_max) # number of loops required - 1 (can't set time above current time)
    for i in range(num_iterations):
        url = f'https://api-pub.bitfinex.com/v2/status/deriv/{symbol}/hist?start={start_iteration}&end={end_iteration}&sort=1&limit=5000'
        response = requests.request("GET", url, headers={}, data={})
        data = response.json()
        
        df = pd.DataFrame(data, columns=col_names) ##
        df = df.groupby(['NEXT_FUNDING_EVT_TIMESTAMP_MS', 'CURRENT_FUNDING'], as_index= False).mean() # groupby
        df['NEXT_FUNDING_EVT_TIMESTAMP_MS'] = pd.to_datetime(df['NEXT_FUNDING_EVT_TIMESTAMP_MS'], unit='ms') #miliseconds
        df.rename(columns = {'NEXT_FUNDING_EVT_TIMESTAMP_MS': 'funding_time'}, inplace=True)
        df_final = df_final.append(df) ##
        
        start_iteration = end_iteration
        end_iteration = start_iteration + call_max
        
        print(df_final)

    # final loop
    end_iteration = dt.datetime(2021,1,1).now().timestamp()*1000
    url = f'https://api-pub.bitfinex.com/v2/status/deriv/{symbol}/hist?start={start_iteration}&end={end_iteration}&sort=1&limit=5000'
    response = requests.request("GET", url, headers={}, data={})
    data = response.json()
    
    df = pd.DataFrame(data, columns=col_names) ##
    df = df.groupby(['NEXT_FUNDING_EVT_TIMESTAMP_MS', 'CURRENT_FUNDING'], as_index= False).mean() # groupby
    df['NEXT_FUNDING_EVT_TIMESTAMP_MS'] = pd.to_datetime(df['NEXT_FUNDING_EVT_TIMESTAMP_MS'], unit='ms') #miliseconds
    df.rename(columns = {'NEXT_FUNDING_EVT_TIMESTAMP_MS': 'funding_time'}, inplace=True)
    df_final = df_final.append(df) ##
    
    df_final = df_final[['funding_time', 'CURRENT_FUNDING']]
    return(df_final)

def export_excel(list_of_pairs):
    writer = pd.ExcelWriter(save_path + filename)
    for i in list_of_pairs:
        df = bitfinex_perp_funding_rates(i, start_time, end_time)
        df.to_excel(writer, sheet_name = symbol[i] + ' Funding Rates')
    
    writer.save()
    print('file Saved')

    
if __name__ == "__main__":
    save_path = "C:/Users/edgar tan/desktop/python outputs/" #file path
    filename = "bitfinex_perp_funding.xlsx" #filename
    
    start_time = int(dt.datetime(2021,6,8,12,0,0).timestamp()*1000) # start time * 1000 -> milliseconds
    end_time = int(dt.datetime(2021,6,14,12,0,0).timestamp()*1000) # end time * 1000 > milliseconds
    symbol = {'tBTCF0:USTF0':'BTC_PERP', 'tETHF0:USTF0':'ETH_PERP'}
    
    export_excel(symbol)