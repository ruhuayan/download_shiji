import requests
import time
from bs4 import BeautifulSoup
import urllib.parse
import re
import os
from kindle_maker import Ebook

BASE_URL = 'https://www.thn21.com'
PATH_HTML = 'html'
PATH_MOBI = 'mobi'
page = requests.get('https://www.thn21.com/wen/famous/27038.html')
soup = BeautifulSoup(page.content, 'html.parser')

links = soup.find_all('a', class_='liebiao')
title = '史记'
ebook = Ebook(title)

for link in links:
    print(link)
    filename = link.get_text()
    filePath = os.path.join(PATH_HTML, '{}.html'.format(filename))
    
    if os.path.isfile(filePath):
        ebook.create_chapter(filename, filePath)
        continue

    # load page
    page = requests.get(urllib.parse.urljoin(BASE_URL, link['href']))
    soup = BeautifulSoup(page.content, 'html.parser')
    # get page content
    content = soup.select('#V')
    if not content:
        content = soup.select('#v')
    if content:
        content[0].div.extract()
        
        if not content[0].p:
            c = BeautifulSoup('<p>{0} - No Content</p>'.format(link.get_text()))
            print(c)
        else: 
            c = content[0]
        
        # remove body innerHTML
        soup.body.clear()
        if soup.head.link:
            soup.head.link.extract()
        soup.body.append(c)
        
        with open(filePath, 'w') as f:
            f.write(soup.prettify())
            chapter = ebook.create_chapter(filename, filePath)

fn = os.path.join(PATH_MOBI, '{}.mobi'.format(title))
with open(fn, 'w') as f:
    for link in links:
        f.write('# {}\n'.format(link.get_text()))     
ebook.save(fn)


