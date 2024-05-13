import requests
import pandas as pd
import json

class zapper:
    
    # https://api.zapper.fi/api/static/index.html - documentation is found here
    
    def __init__(self):
        self.apikey = '03c68197-90bb-4a53-b11f-2b286ac61450'
        self.base_url = 'https://api.zapper.fi' # base url
    
    def get_balances(self, address: str, network: str):
        """
        apps
        
        """
        
        endpoint = '/v2/balances'
        # headers = {'api_key': self.apikey}
        headers = {'Authorization': 'Basic MDNjNjgxOTctOTBiYi00YTUzLWIxMWYtMmIyODZhYzYxNDUwOg=='}
        params = {'addresses[]': address, 'networks[]': network, 'bundled': False,}
        
        response = requests.get(self.base_url + endpoint, headers = headers, params = params)
        print(response.url)
        print(response.headers)
        return response
        
if __name__ == "__main__":
    
    client = zapper()
    
    address = '0xbe0eb53f46cd790cd13851d5eff43d12404d33e8'
    network = 'ethereum'
    balance = client.get_balances(address, network)
