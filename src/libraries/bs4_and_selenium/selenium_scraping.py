# pip install selenium
# pip install webdriver-manager

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.get('https://portfolio.nansen.ai/dashboard/binance')

# needs time to load data
time.sleep(15)

search = driver.find_element(By.TAG_NAME, 'h1')
m2m = search.text

m2m = m2m.replace('$', '')
m2m = m2m.replace(',', '')
m2m = float(m2m)
print(m2m)

driver.quit()
# driver.close()