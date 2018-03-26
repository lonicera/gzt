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

    def getColumunists(self):
        data = getPage(self.adress)
        thelist = data.find('div', {'class': 'module-default-todayArticles'}).find('ul').find_all('li')
        clist = []
        for i in thelist:
            y = []
            link = i.find('a').get('href')
            title = i.find('a').get('title')
            image = i.find('img').get('src')
            name = i.find('img').get('alt')
            y.append([link, title, image, name])
            clist.extend(y)
        return clist

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

    def getColumunists(self):
        data = getPage(self.adress + '/kategori/yazarlar/')
        thelist = data.find_all('div', {'class':'clearfix'})[0].find_all('div', {'class': 'news-box'})
        clist = []
        for i in thelist:
            y = []
            link = i.find('a').get('href')
            title = i.find('div', {'class':'c-text'}).text
            image = i.find('span', {'class':'news-img'})['style'].split('(')[1].split(')')[0]
            name = i.find('div', {'class':'columnist-name'}).text
            y.append([link, title, image, name])
            clist.extend(y)
        return clist

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

    def getColumunists(self):
        data = getPage(self.adress + '/yazarlar/')
        thelist = data.find('div', {'data-list-type' : 'author'}).find_all('a', {'class' : 'author-box'})
        clist = []
        for i in thelist:
            y = []
            link = i.get('href')
            title = i.get('title')
            image = i.find('img').get('src')
            name = i.find('span', {'class' : 'name'}).text
            y.append([link, title, image, name])
            clist.extend(y)
        return clist

class Haberler:
    def __init__(self):
        self.name = 'Haberler.com'
        self.adress = 'http://www.haberler.com/'
        self.container = 'haberler-news'

    def parseNewsList(self):
        data = getPage(self.adress)
        thelist = data.find_all('ul', {'class' : self.container})
        newslist = []
        for i in thelist:
            y = []
            news_id = i.find('a').get('href').split('-')[-2:-1]
            try:
                if news_id[0].isdigit() and int(news_id[0]) > 100 :
                    news_link = i.find('a').get('href')
                    news_picture = i.find('img', {'class' : 'lazy'}).get('data-original')
                    news_title = i.find('a').get('title')
                    print(news_title)
                    y.append([news_title, news_link, news_picture, news_id])
                newslist.extend(y)
            except:
                pass
        return newslist

    def parseNewsContent(self, url):
        data = getPage(url)
        thenews = data.find('div', {'class': 'haber_metni'})
        text = ""
        for i in thenews.find_all('p'):
            text = text + " " + i.text + " "
        return data.find('h1').text, data.find('h2').text, text
