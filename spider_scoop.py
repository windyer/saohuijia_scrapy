#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-02-06 17:22:55
# Project: scoop

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
            "http://www.scoop.co.nz/storyindex/index.rss?s.c=BU":"business",
            "http://www.scoop.co.nz/storyindex/index.rss?s.c=SC":"sci-tech",
            "http://www.scoop.co.nz/storyindex/index.rss?s.c=PA":"parliament",
            "http://www.scoop.co.nz/storyindex/index.rss?s.c=PO":"politics",
            "http://www.scoop.co.nz/storyindex/index.rss?s.c=AK":"regional",
            "http://www.scoop.co.nz/storyindex/index.rss?s.c=WO":"world",
            "http://www.scoop.co.nz/storyindex/index.rss?s.c=CU":"culture",
            "http://www.scoop.co.nz/storyindex/index.rss?s.c=ED":"education",
            "http://www.scoop.co.nz/storyindex/index.rss?s.c=GE":"general",
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
        title = tree.xpath("//h1/text()")
        article_time = tree.xpath("//span[@class='byline']//b/text()")
        images = tree.xpath("//p//img/@src")
        soup = BeautifulSoup(response.content)
        text = soup.select('p')
        content = str(text[1])
        soup2 = BeautifulSoup(content)
        #s=[s.extract() for s in soup2('script')]
        imgs =soup2.select('img')
        content2 = str(soup2)
        content = str(soup2)
        images2=[]
        for img,img2 in zip(imgs,images):
                new_image = update.load(img, "scoop")
                images2.append(new_image)
                content = content.replace(img, new_image)
                content2 = content2.replace(str(img2),"(url,"+str(new_image)+")")
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
            "AddTime": str(datetime.datetime.strptime(article_time[1],' %d %B %Y').date()),
            "Images": ",".join(images2),
            "ImageNum": len(images2),
            "Language": 1,
            "NewsSource": "scoop",
            "Link": response.url,
            "PlainText":text,
        }
        #sql.into(**data)
        return data