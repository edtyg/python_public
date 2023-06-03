import requests
import pandas as pd
import urllib.parse

class zapper:
    
    # https://api.zapper.fi/api/static/index.html - documentation is found here
    
    def __init__(self):
        self.apikey = '96e0cc51-a62e-42ca-acee-910ea7d2a241' # standard api key for public use
        self.base_url = 'https://api.zapper.fi' # base url
    
    def get_apps(self):
        """
        apps
        
        """
        
        endpoint = '/v1/apps'
        params = {'api_key': self.apikey}
        
        
        r = requests.request(
            'GET', 
            self.base_url + endpoint, 
            params = params,
            )
        
        data = r.json()
        df = pd.DataFrame(data)
        return(df)
    
    def get_apps_byid(self, appid: str):
        """
        apps
        
        """
        
        endpoint = f'/v1/apps/{appid}'
        params = {'api_key': self.apikey}
        
        r = requests.request(
            'GET', 
            self.base_url + endpoint, 
            params = params,
            )
        
        data = r.json()
        return(data)
    
    def get_protocol_balances(self, appid: str, my_wallet_address: str, network: str):
        
        endpoint = f'/v1/protocols/{appid}/balances'
        params = {
            'addresses[]': my_wallet_address,
            'network': network,
            'api_key': self.apikey,
            }
 
        r = requests.request(
            'GET', 
            self.base_url + endpoint, 
            params = params,
            )
        print(r.url)
        
        data = r.json()
        return(data)
    
        
if __name__ == "__main__":
    
    client = zapper()
    
    # apps = client.get_apps()
    # apps_uniswapv2 = client.get_apps_byid('uniswap-v2')
    
    appid = 'uniswap-v2'
    my_wallet_address = '0x26620de94599aBcEB543e910764B71Be6c4D456C'
    network = 'ethereum'
    uniswap_bal = client.get_protocol_balances(appid, my_wallet_address, network)
