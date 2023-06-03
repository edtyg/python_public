import requests
from bs4 import BeautifulSoup


def get_exchange_reserves(exchange_dict: dict):
    
    exchange_reserves = {}
    
    for exchange in exchange_dict:
        print(exchange)
        if exchange_dict[exchange] == 'spot':
            url = f'https://coinmarketcap.com/exchanges/{exchange}/'
        elif exchange_dict[exchange] == 'deriv':
            url = f'https://coinmarketcap.com/exchanges/{exchange}/?type=perpetual'
            
        resp = requests.get(url)
        html = resp.text
        
        soup = BeautifulSoup(html, 'html.parser')
        html_element = soup.find_all('span', {"data-sensors-click": "true", "class": "sc-e225a64a-0 eUsFBk priceText" })
        data = list(html_element) # 2 elements with same class
        m2m_value = data[1].text # taking the last 1
        
        m2m_value = m2m_value.replace('$', '')
        m2m_value = m2m_value.replace(',', '')
        m2m_value = float(m2m_value)
        
        exchange_reserves[exchange] = m2m_value
        print(m2m_value)
        
    return(exchange_reserves)

if __name__ == "__main__":
    exchange_dict = {
        'binance': 'spot',
        'okx': 'spot',
        'crypto-com-exchange': 'spot',
        'kucoin': 'spot',
        'bitfinex': 'spot',
        'huobi': 'spot',
        'bybit': 'spot',
        'deribit': 'deriv',
        }
    
    m2m_value = get_exchange_reserves(exchange_dict)
    print(m2m_value)