#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-15 16:42:02
# Project: jiemian

from pyspider.libs.base_handler import *
from newspaper import Article
from lxml import etree

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

    @config(age=10 * 24 * 60 * 60)
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
        time = tree.xpath("//span[@class='date']/text()")
        return {
            "title": article.title,
            "text": article.text,
            "image":article.images[0:3],
            "time":time[0]
        }
