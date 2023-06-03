# for websites with data already loaded this works
# otherwise use selenium with a driver

import requests
from bs4 import BeautifulSoup

url = 'https://portfolio.nansen.ai/dashboard/binance'

resp = requests.get(url, verify = False, timeout=None)
html = resp.text

soup = BeautifulSoup(html, 'html.parser')
print(soup)