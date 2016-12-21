#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-16 16:43:58
# Project: chinaconsulate
from newspaper import Article
from pyspider.libs.base_handler import *
from lxml import etree
from mysql_conf import ToMysql
import time

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.chinaconsulate.org.nz/chn/xwdt/', callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if "htm" in each.attr.href:
                self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        url = response.url
        article = Article(url, language='zh')
        article.download()
        article.parse()
        content = response.content
        tree = etree.HTML(content)
        article_time = tree.xpath("//div[@id='News_Body_Time']/text()")
        images = article.images
        sql = ToMysql()
        data = {
            "title": article.title,
            "text":article.text,
            "article_time":"".join(article_time),
            "spider_time":time.strftime('%Y-%m-%d %H:%M:%S'),
            "image_1": images[0] if len(images) >= 1 else None,
            "image_2": images[1] if len(images) >= 2 else None,
            "image_3": images[2] if len(images) >= 3 else None,
            "source": "chinaconsulate",
            "tab":0,
        }
        sql.into(**data)
        return data