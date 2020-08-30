import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
from ebook import Chapter, Ebook

BASE_URL = 'https://zh.m.wikisource.org/wiki/%E9%87%91%E7%93%B6%E6%A2%85'
PATH_HTML = 'output'
PATH_MOBI = 'mobi'
page = requests.get('https://zh.m.wikisource.org/wiki/%E9%87%91%E7%93%B6%E6%A2%85')
soup = BeautifulSoup(page.content, 'html.parser')

links = soup.find('table', class_='multicol').find_all('a')
title = '金瓶梅'

def download():
    
    ebook = Ebook(PATH_HTML, title)

    for link in links:
        print(link)

        chapter_name = link.get_text()
        page = requests.get(urllib.parse.urljoin(BASE_URL, link['href']))
        soup = BeautifulSoup(page.content, 'html.parser', from_encoding="gb18030")

        # create chapter header
        chapter = Chapter(chapter_name)

        chapter_content = get_content(soup)

        chapter.set_content(chapter_content)
        ebook.add_chapter(chapter)

    ebook.save()
def get_content(soup):
    c = BeautifulSoup()
    section = soup.find('section', class_='mf-section-0')
    ps = section.find_all('p')
    for p in ps:
        c.append(p)
        
    return c
if __name__ == '__main__': 
    download()