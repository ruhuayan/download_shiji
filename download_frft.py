import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
from ebook import Chapter, Ebook

BASE_URL = 'http://www.dushu369.com'
page = requests.get('http://www.dushu369.com/zhongguomingzhu/myzpj/frft/')
soup = BeautifulSoup(page.content, 'html.parser', from_encoding="gb18030")

links = soup.find('td', class_='content').find_all('a')
title = '丰乳肥臀'

def download():
    
    ebook = Ebook(title)

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
    section = soup.find('td', class_='content')
    ps = section.find_all('p')
    for p in ps:
        c.append(p)
        
    return c
if __name__ == '__main__': 
    download()