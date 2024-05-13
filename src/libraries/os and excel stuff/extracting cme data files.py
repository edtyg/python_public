import os
import pandas as pd

filepath = 'C:/Users/Administrator/OneDrive/Desktop/2022 CME DATA/'
months = os.listdir(filepath)

# f files are final files sent the morning of the next trade date
# p files are preliminary file sent at end of trade date
# e files are earliest files sent

# 20221230-EOD_xcme_mbt_fut_eth_f.csv - micro bitcoin futures
# 20221230-EOD_xcme_mbt_fut_eth_p.csv - micro bitcoin futures
# 20221230-EOD_xcme_mbt_fut_rth_e.csv - micro bitcoin futures

# 20221230-EOD_xcme_met_fut_eth_f.csv - micro ether futures
# 20221230-EOD_xcme_met_fut_eth_p.csv - micro ether futures
# 20221230-EOD_xcme_met_fut_rth_e.csv - micro ether futures

# 20221230-EOD_xcme_obc_opt_eth_f.csv - options on bitcoin futures
# 20221230-EOD_xcme_obc_opt_eth_p.csv - options on bitcoin futures
# 20221230-EOD_xcme_obc_opt_rth_e.csv - options on bitcoin futures

# 20221230-EOD_xcme_vm_opt_eth_f.csv - mthly option on micro eth fut
# 20221230-EOD_xcme_vm_opt_eth_p.csv - mthly option on micro eth fut
# 20221230-EOD_xcme_vm_opt_rth_e.csv - mthly option on micro eth fut

def select_csv_files(l: list):
    # filtering out f.csv files
    # f = final files
    
    new_list = []
    
    for i in l:
        if i.endswith('f.csv'):
            new_list.append(i)
    return(new_list)

file_directories = []
for month in months:
    month_filepath = filepath + month
    
    days = os.listdir(month_filepath)
    for day in days:
        day_filepath = month_filepath + '/' + day + '/EOD' + '/XCME'
        
        files = os.listdir(day_filepath)
        files = select_csv_files(files)
        for file in files:
            csv_files = day_filepath + '/' + file
            file_directories.append(csv_files) # list of f.csv files
            print(csv_files) 

# combine all into dataframes
df_mbtc_fut = pd.DataFrame()
df_meth_fut = pd.DataFrame()
df_opt_btc_fut = pd.DataFrame()
df_mth_opt_meth_fut = pd.DataFrame()

for file in file_directories:
    
    if file.endswith('mbt_fut_eth_f.csv'):
        df = pd.read_csv(file)
        df_mbtc_fut = pd.concat([df_mbtc_fut, df])
    
    elif file.endswith('met_fut_eth_f.csv'):
        df = pd.read_csv(file)
        df_meth_fut = pd.concat([df_meth_fut, df])
    
    elif file.endswith('obc_opt_eth_f.csv'):
        df = pd.read_csv(file)
        df_opt_btc_fut = pd.concat([df_opt_btc_fut, df])
    
    elif file.endswith('vm_opt_eth_f.csv'):
        df = pd.read_csv(file)
        df_mth_opt_meth_fut = pd.concat([df_mth_opt_meth_fut, df])
    
extract_filepath = 'C:/Users/Administrator/OneDrive/Desktop/'
df_mbtc_fut.to_csv(extract_filepath + 'mbtc_fut.csv')
df_meth_fut.to_csv(extract_filepath + 'meth_fut.csv')
df_opt_btc_fut.to_csv(extract_filepath + 'opt_btc_fut.csv')
df_mth_opt_meth_fut.to_csv(extract_filepath + 'mth_opt_meth_fut.csv')
    