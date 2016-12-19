#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-15 16:42:02
# Project: jiemian

from pyspider.libs.base_handler import *
from newspaper import Article
from lxml import etree
from mysql_conf import ToMysql
import time

class Handler(BaseHandler):
    crawl_config = {
    }
    def __init__(self):
        self.page = 50

    @every(minutes=24 * 60)
    def on_start(self):
        urls=[]
        url="http://a.jiemian.com/index.php?m=search&a=index&msg=%E6%96%B0%E8%A5%BF%E5%85%B0&type=news&page={}"
        for i in range(self.page):
            urls.append(url.format(str(i+1)))
        self.crawl(urls, callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            detail_url = each.attr.href
            if ("article" in detail_url) and ("html" in detail_url):
                self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        url = response.url
        article=Article(url,language='zh')
        article.download()
        article.parse()
        tree = etree.HTML(response.content)
        article_time = tree.xpath("//span[@class='date']/text()")
        images = tree.xpath("//div[@class='article-main']//img/@src")
        sql = ToMysql()
        data = {
            "title": article.title,
            "text": article.text,
            "article_time": article_time[0],
            "spider_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "image_1": images[0] if len(images) >= 1 else None,
            "image_2": images[1] if len(images) >= 2 else None,
            "image_3": images[2] if len(images) >= 3 else None,
            "source": "jiemian",
        }
        sql.into(**data)
        return data

