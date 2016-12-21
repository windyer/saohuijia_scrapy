#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-19 10:06:22
# Project: kannz
from lxml import etree
from pyspider.libs.base_handler import *
from mysql_conf import ToMysql
import time

class Handler(BaseHandler):
    crawl_config = {
    }
    def __init__(self):
        self.page_cout = 10
        self.url = "http://www.kannz.com/page/{0}/"
    @every(minutes=24 * 60)
    def on_start(self):
        for page in range(self.page_cout):
            url = self.url.format(str(page+1))
            self.crawl(url, callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        urls = tree.xpath("//article[@class='excerpt']//header//h2//a/@href")
        urls2 = []
        for i in urls:
            urls2.append(i)
        self.crawl(urls2, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        tree = etree.HTML(response.content)
        article_time = tree.xpath("//time[@class='muted']/text()")
        txt = tree.xpath("//p/text()")
        title = tree.xpath("//h1[@class='article-title']//a/text()")
        images = tree.xpath("//article[@class='article-content']//img/@src")
        sql = ToMysql()
        data = {
            "title": "".join(title),
            "text": "".join(txt),
            "article_time": "".join(article_time),
            "spider_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "image_1": images[0] if len(images) >= 1 else None,
            "image_2": images[1] if len(images) >= 2 else None,
            "image_3": images[2] if len(images) >= 3 else None,
            "source": "kannz",
            "tab": 0,
        }
        sql.into(**data)
        return data

