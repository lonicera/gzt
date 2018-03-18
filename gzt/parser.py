#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

import urllib3

def getPage(url):
    http = urllib3.PoolManager()
    page = http.request('GET', url)
    source = BeautifulSoup(page.data, "html.parser")
    return source

class Alert:
    def __init__(self):
        self.keywords = ['raspberry', 'linux', 'afrin', 'ABD']
    
class YeniAkit:
    def __init__(self):
        self.name = 'YeniAkit'
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
        self.newsListContainer = 'swiper-slide'
        
    def parseNewsList(self):
        data = getPage(self.adress)
        newslistdata = data.find_all('div', {'class': self.newsListContainer})
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
            text = text + " " + i.text
        return data.find('h1').text, data.find('h2').text, text

class Milliyet:
    def __init__(self):
        self.adress = 'http://www.milliyet.com.tr'
        self.container = 'carousel11'
    
    def parseNewsList(self):
        data = getPage(self.adress)
        for i in data.find('div', {'id': self.container }).find_all('a'):
            print(i.get('href'))
        
        
        
#print(YeniakIT().parseNewsContent('http://www.yeniakit.com.tr/haber/almanyadan-turkiyeye-kustah-afrin-cagrisi-429537.html'))
#print(Sozcu().parseNewsList())
