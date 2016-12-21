#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-15 17:34:08
# Project: toutiao
import time
from pyspider.libs.base_handler import *
import json
from newspaper import Article
from lxml import etree
from mysql_conf import ToMysql
import time
class Handler(BaseHandler):
    crawl_config = {
    }
    def __init__(self):
        self.cont = "500"

    @every(minutes=24 * 60)
    def on_start(self):
        url = "http://www.toutiao.com/search_content/?offset=0&format=json&keyword=%E6%96%B0%E8%A5%BF%E5%85%B0&autoload=true&count={0}&_=1478682405913".format(self.cont)
        self.crawl(url, callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):
        #for each in response.doc('a[href^="http"]').items():
        content = response.content
        js_data = json.loads(content)
        data = js_data['data']
        for article_data in data:
            self.crawl(article_data['article_url'], callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        url = response.url
        article = Article(url, language='zh')
        article.download()
        article.parse()
        tree = etree.HTML(response.content)
        article_time = tree.xpath("//span[@class='time']/text()")
        title = tree.xpath("//h1[@class='article-title']/text()")
        title2 = tree.xpath("//title/text()")
        images = tree.xpath("//div[@id='article-main']//img/@src")
        sql = ToMysql()
        data = {
            "title": "".join(title) if len("".join(title))>0 else "".join(title2),
            "text": article.text,
            "article_time": "".join(article_time),
            "spider_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "image_1": images[0] if len(images) >= 1 else None,
            "image_2": images[1] if len(images) >= 2 else None,
            "image_3": images[2] if len(images) >= 3 else None,
            "source": "toutiao",
            "tab":0,
        }
        sql.into(**data)
        return data
