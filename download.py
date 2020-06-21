import requests
# import time
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
    for link in links[104:]:
        print(link)
        filename = link.get_text()
        filePath = os.path.join(ebook.output_path, PATH_HTML, '{}.html'.format(filename))
        
        if os.path.isfile(filePath):
            ebook.create_chapter(filename, filePath)
            # continue

        # load page
        page = requests.get(urllib.parse.urljoin(BASE_URL, link['href']))
        soup = BeautifulSoup(page.content, 'html.parser', from_encoding="gb18030")
        pageLink = soup.find('p', class_='pageLink') #.find_all('a', href=True)

        if pageLink:
            sub_pages = pageLink.find_all('a', href=True)
            pageLink.extract()

        c = get_content(soup)
        soup.body.clear()
        if soup.head.link:
            soup.head.link.extract()
        
        # if there are sub pages
        if sub_pages:
            hrefs = [l['href'] for l in sub_pages]
            hrefs = list(set(hrefs))
            hrefs.sort()
            print(hrefs)
            index = 0
            for href in hrefs:
                index += 1
                print(index)
                sub_page = requests.get(urllib.parse.urljoin(BASE_URL, href))
                soup_link = BeautifulSoup(sub_page.content, 'html.parser', from_encoding="gb18030")
                sub_cont = get_content(soup_link)
                c.append(sub_cont)
        soup.body.append(c)
            
        with open(filePath, mode='w', encoding='utf-8') as f:
            print(filePath)
            f.write(soup.prettify())
            ebook.create_chapter(filename, filePath) 
    # ebook.save()

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
    index = 0
    for link in links:
        print(link)
        chapter_name = link.get_text()
        page = requests.get(urllib.parse.urljoin(BASE_URL, link['href']))
        soup = BeautifulSoup(page.content, 'html.parser', from_encoding="gb18030")

        # create chapter header
        index = index + 1
        chapter_header = BeautifulSoup('<mbp:pagebreak/><h2 id="chapter-{}">{}</h2>'.format(index, chapter_name))
        soup_doc.body.append(chapter_header)

        pageLink = soup.find('p', class_='pageLink') #.find_all('a', href=True)
        sub_pages = None
        if pageLink:
            sub_pages = pageLink.find_all('a', href=True)
            pageLink.extract()

        c = get_content(soup)

        # if there are sub pages
        if sub_pages:
            hrefs = [l['href'] for l in sub_pages]
            hrefs = list(set(hrefs))
            hrefs.sort()
            print(hrefs)
            j = 0
            for href in hrefs:
                j += 1
                print(j)
                sub_page = requests.get(urllib.parse.urljoin(BASE_URL, href))
                soup_link = BeautifulSoup(sub_page.content, 'html.parser', from_encoding="gb18030")
                sub_cont = get_content(soup_link)
                c.append(sub_cont)
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
    content = soup.select('#V') or soup.select('#v')

    # if not content:
    #     content = soup.select('#v')
    if content:
        content[0].div.extract()
    
    if not content[0].p:
        paragraphes = soup.find_all('p')
        c = BeautifulSoup()
        for p in paragraphes:
            if p.find('a'):
                break
            c.append(p)
        # print(c)
    else: 
        c = content[0]
    return c

if __name__ == '__main__': 
    download_onefile()