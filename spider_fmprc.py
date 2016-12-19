#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-15 15:22:33
# Project: fmprc

from pyspider.libs.base_handler import *
from newspaper import Article
from lxml import etree
from mysql_conf import ToMysql
import time

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.fmprc.gov.cn/wjb/web_search.jsp?presearchword=&channelid=75003&siteid=5243&prepage=500&page=1&searchword=%E6%96%B0%E8%A5%BF%E5%85%B0+and+siteid%3D5243&sw=%E6%96%B0%E8%A5%BF%E5%85%B0&select=1', callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            detail_url=each.attr.href
            if "html" in detail_url:
                self.crawl(detail_url, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        url = response.url
        article=Article(url,language='zh')
        article.download()
        article.parse()
        tree = etree.HTML(response.content)
        article_time = tree.xpath("//span[@id='News_Body_Time']/text()")
        images= []
        for image in article.images:
            if "jpg" in image:
                images.append(image)
        sql = ToMysql()
        data = {
            "title": article.title,
            "text": article.text,
            "article_time": "".join(article_time),
            "spider_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "image_1": images[0] if len(images) >= 1 else None,
            "image_2": images[1] if len(images) >= 2 else None,
            "image_3": images[2] if len(images) >= 3 else None,
            "source": "fmprc",
        }
        sql.into(**data)
        return data

