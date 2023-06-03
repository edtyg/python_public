# saved a copy of html file from nansen - with data loaded

from bs4 import BeautifulSoup

with open('nansen.htm', 'r') as html_file:
    content = html_file.read()
    
    soup = BeautifulSoup(content, 'html')
    print(soup)
    html_element = soup.find('h1')
    value = html_element.text

# muitypography-root muitypography-h1 css-dreoll