import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
from ebook import Chapter, Ebook

BASE_URL = 'https://www.thn21.com'
page = requests.get('https://www.thn21.com/wen/famous/27038.html')
soup = BeautifulSoup(page.content, 'html.parser')

links = soup.find_all('a', class_='liebiao')
title = '史记'

def download():
    
    ebook = Ebook(title)

    for link in links:
        print(link)
        chapter_name = link.get_text()
        page = requests.get(urllib.parse.urljoin(BASE_URL, link['href']))
        soup = BeautifulSoup(page.content, 'html.parser', from_encoding="gb18030")

        # create chapter header
        chapter = Chapter(chapter_name)

        pageLink = soup.find('p', class_='pageLink')
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

            for href in hrefs:
                
                sub_page = requests.get(urllib.parse.urljoin(BASE_URL, href))
                soup_link = BeautifulSoup(sub_page.content, 'html.parser', from_encoding="gb18030")
                sub_cont = get_content(soup_link)
                c.append(sub_cont)
        chapter.set_content(str(c))
        ebook.add_chapter(chapter)

    ebook.save()
    
def get_content(soup):
    # get page content
    content = soup.select('#V') or soup.select('#v')

    if content:
        content[0].div.extract()
    
    if not content[0].p:
        paragraphes = soup.find_all('p')
        c = BeautifulSoup()
        for p in paragraphes:
            if p.find('a'):
                break
            c.append(p)
    else: 
        c = content[0]
    return c

if __name__ == '__main__': 
    download()