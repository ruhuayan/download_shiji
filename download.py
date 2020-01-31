import requests
import time
import pdfkit
from bs4 import BeautifulSoup
import urllib.parse
import re

BASE_URL = 'https://www.thn21.com'
page = requests.get('https://www.thn21.com/wen/famous/27038.html')
soup = BeautifulSoup(page.content, 'html.parser')

links = soup.find_all('a', class_='liebiao')
html = ''
# for link in links:
#     print(link)
#     page = requests.get(urllib.parse.urljoin(BASE_URL, link['href']))
#     # time.sleep(1)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     content = soup.select('#V')
#     if not content:
#         content = soup.select('#v')
#     if content:
#         content[0].div.extract()
        
#         if not content[0].p:
#             c = '<p>{0} - No Content</p>'.format(link.get_text())
#             print(c)
#         else: 
#             c = content[0].get_text()
        
#         html += c
    
link = links[0]
page = requests.get(urllib.parse.urljoin(BASE_URL, link['href']))
soup = BeautifulSoup(page.content, 'html.parser')
content = soup.select('#V')

html = content[0].get_text()
pdfkit.from_string('Hello!', 'out.pdf')


