import requests
import time
from bs4 import BeautifulSoup
import urllib.parse
import re
import os
from ebook import Ebook

BASE_URL = 'https://www.thn21.com'
PATH_HTML = 'html'
PATH_MOBI = 'mobi'
page = requests.get('https://www.thn21.com/wen/famous/27038.html')
soup = BeautifulSoup(page.content, 'html.parser')

links = soup.find_all('a', class_='liebiao')
title = '史记'

def download():
    ebook = Ebook(PATH_MOBI, title)
    for link in links:
        print(link)
        filename = link.get_text()
        filePath = os.path.join(ebook.output_path, PATH_HTML, '{}.html'.format(filename))
        
        if os.path.isfile(filePath):
            ebook.create_chapter(filename, filePath)
            continue

        # load page
        page = requests.get(urllib.parse.urljoin(BASE_URL, link['href']))
        soup = BeautifulSoup(page.content, 'html.parser', from_encoding="gb18030")
    
        c = get_content(soup)
        soup.body.clear()
        if soup.head.link:
            soup.head.link.extract()
        soup.body.append(c)
            
        with open(filePath, mode='w', encoding='utf-8') as f:
            f.write(soup.prettify())
            ebook.create_chapter(filename, filePath) 
    ebook.save()

def download_onefile():
    import subprocess
    doc = '''
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
        <title>{}</title>
    </head>
    <body>
    </body>
    </html>
    '''.format(title)
    soup_doc = BeautifulSoup(doc, 'html.parser')

    for link in links:
        print(link)
        chapter_name = link.get_text()
        page = requests.get(urllib.parse.urljoin(BASE_URL, link['href']))
        soup = BeautifulSoup(page.content, 'html.parser', from_encoding="gb18030")

        # create chapter header
        chapter_header = BeautifulSoup('<h2>{}</h2>'.format(chapter_name))
        soup_doc.body.append(chapter_header)

        c = get_content(soup)
        soup_doc.body.append(c)

    file_path = os.path.join(PATH_HTML, '{}.html'.format(title))
    with open(file_path, mode='w', encoding='utf-8') as f:
            f.write(soup_doc.prettify())
    # ebook-convert html to mobi
    rc = subprocess.call([
        'ebook-convert', file_path, os.path.join(PATH_HTML, '{}.mobi'.format(title)) 
    ])
    if rc != 0:
        raise Exception('ebook-convert failed')
    
def get_content(soup):
    # get page content
    content = soup.select('#V')

    if not content:
        content = soup.select('#v')
    if content:
        content[0].div.extract()
    
    if not content[0].p:
        c = BeautifulSoup('<p>No Content</p>')
        print(c)
    else: 
        c = content[0]
    return c

if __name__ == '__main__': 
    download_onefile()