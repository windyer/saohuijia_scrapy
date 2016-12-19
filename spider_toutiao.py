#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-15 17:34:08
# Project: toutiao
import time
from pyspider.libs.base_handler import *
import json
from newspaper import Article
from lxml import etree

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
        #time = tree.xpath("//span[@class='time']/text()")
        title = tree.xpath("//h1[@class='article-title']/text()")
        return {
            "text": article.text,
            "title":title[0].encode("utf-8") ,
            "image":article.images[0:2],
            "time":time.strftime('%Y-%m-%d %H:%M:%S'),
        }
