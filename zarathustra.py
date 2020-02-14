import requests
import time
from bs4 import BeautifulSoup
import urllib.parse
import re
import os

def download():
    import subprocess
    PATH_HTML = 'html'
    title = 'zarathustra'
    file_path = os.path.join(PATH_HTML, 'zarathustra.html')

    contents = open(file_path).read()
    soup = BeautifulSoup(contents, 'html.parser')
    links = soup.find_all('span', class_='mw-editsection')
    print(len(links))
    for link in links:
        # print(link)
        link.extract()

    open(file_path, 'w').write(soup.prettify())
    # ebook-convert html to mobi
    rc = subprocess.call([
        'ebook-convert', file_path, os.path.join(PATH_HTML, '{}.mobi'.format(title)) 
    ])
    if rc != 0:
        raise Exception('ebook-convert failed')

if __name__ == '__main__': 
    download()