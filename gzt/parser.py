#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

import urllib3

def getPage(url):
    http = urllib3.PoolManager()
    page = http.request('GET', url)
    source = BeautifulSoup(page.data, "html.parser")
    return source

class YeniAkit:
    def __init__(self):
        self.name = 'Yeni Akit'
        self.adress = 'http://www.yeniakit.com.tr'
        self.newsListContainer = 'indicators'

    def parseNewsList(self):
        data = getPage(self.adress)
        newslistOL = data.find('ol',{'class': self.newsListContainer}).find_all('li')
        newslist = []
        newlist = []
        for i in newslistOL:
            y = []
            if  i.find('a').get('title') is not None:
                news_id = int(i.find('a').get('href').split('-')[-1].split('.')[0])
                y.append([i.find('a').get('title'), i.find('a').get('href'), i.find('a').get('data-image'), news_id])
            newslist.extend(y)
        return newslist

    def parseNewsContent(self, url):
        data = getPage(url)
        section = data.find('section', {'class':'entry'})
        section.h1 = section.find('h1').text
        section.h2 = section.find('h2').text
        section.article = section.find('article').text
        return section.h1, section.h2, section.article

class Sozcu:
    def __init__(self):
        self.name = 'Sözcü'
        self.adress = 'http://www.sozcu.com.tr'
        self.newsListContainer = 'sz_manset'

    def parseNewsList(self):
        data = getPage(self.adress)
        newslistdata = data.find('div', {'id': self.newsListContainer}).find_all('div', {'class': 'swiper-slide'})
        newslist = []
        for i in newslistdata:
            y = []
            if 'gundem' in i.find('a').get('href') or 'dunya' in i.find('a').get('href'):
                news_id = i.find('a').get('data-postid')
                y.append([i.find('a').get('title'), i.find('a').get('href') , i.find('img').get('src'), news_id])
            newslist.extend(y)
        return newslist

    def parseNewsContent(self, url):
        data = getPage(url)
        data.find('h2').text
        thenews = data.find('div', {'class': 'content-element'}).find_all('p')
        text = ""
        for i in thenews:
            text = text + " " + i.text + " "
        return data.find('h1').text, data.find('h2').text, text

class Hurriyet:
    def __init__(self):
        self.name = 'Hürriyet'
        self.adress = 'http://www.hurriyet.com.tr/'
        self.container = 'swiper-wrapper'

    def parseNewsList(self):
        data = getPage(self.adress)
        newslistdata = data.find_all('div', {'class': self.container})
        newslist = []
        for i in newslistdata[1]:
            news_id = i.find('a').get('data-news-id')
            news_link = i.find('a').get('href')
            y = []
            if news_id != "-1" and not "galeri" in news_link and not "yazarlar" in news_link and not "magazin" in news_link and not "dunya" in news_link and not "ekonomi" in news_link:
                news_picture = i.find('img').get('src')
                news_title = i.find('img').get('alt')
                y.append([news_title, news_link, news_picture, news_id])
            newslist.extend(y)
        return newslist

    def parseNewsContent(self, url):
        data = getPage(self.adress + url)
        data.find('h1').text
        data.find('h2').text
        thenews = data.find_all('div', {'class': 'news-box'})
        text = ""
        for i in thenews[2].find_all('p'):
            text = text + " " + i.text + " "
        return data.find('h1').text, data.find('h2').text, text
