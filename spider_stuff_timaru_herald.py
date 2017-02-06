#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-26 15:12:28
# Project: timaru-herald

from newspaper import Article
from pyspider.libs.base_handler import *
from xml.etree import ElementTree
from lxml import etree
from mysql_conf import ToMysql
import time,datetime
from bs4 import BeautifulSoup
from mysql_conf import FormatContent
import timer
from qiniu_update import update
import re

class Handler(BaseHandler):
    crawl_config = {
    }
    def __init__(self):
        self.urls={
            "http://www.stuff.co.nz/rss/timaru-herald" : "timaru-herald",
        }

    @every(minutes=24 * 60)
    def on_start(self):
        for url in self.urls.keys():
            self.crawl(url, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        content = response.content
        root = ElementTree.fromstring(content)
        lst_node = root.getiterator("link")
        for i in lst_node:
            self.crawl(i.text, callback=self.detail_page)
    @config(priority=2)
    def detail_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        images = tree.xpath("//article[@class='story_landing']//img/@src")
        t = 0
        title = tree.xpath("//h1/text()")
        article_time = tree.xpath("//span[@itemprop='datePublished']/text()")
        soup = BeautifulSoup(response.content)
        text = soup.select('article[class="story_landing"]')
        content = str(text[0])
        soup2 = BeautifulSoup(content)
        s=[s.extract() for s in soup2('script')]
        s=[s.extract() for s in soup2('span')]
        imgs =soup2.select('img')
        content2 = str(soup2)
        content = str(soup2)
        for img,img2 in zip(imgs,images):
            content=content.replace(img['src'],img2.encode("utf8"))
            content2 = content2.replace(str(img),"(url,"+img2.encode("utf8")+")")
        text_list = []
        for i in BeautifulSoup(content2).findAll(text=True):
            if i !='\n':
                text_list.append(i)
        text = ''.join(text_list)
        #sql = ToMysql()
        format_content = FormatContent()
        article_time = article_time[0].split(",")
        data = {
            "Title": "".join(title).replace("\n","").strip() ,
            "Content": format_content.format_content(content),
            "AddTime": str(datetime.datetime.strptime(article_time[-1],' %B %d %Y').date()),
            "Images": ",".join(images),
            "ImageNum": len(images),
            "Language": 1,
            "NewsSource": "timaru-herald",
            "Link": response.url,
            "PlainText":re.sub('\n+','\n',text.replace("  ","")),
        }
        #sql.into(**data)
        return data