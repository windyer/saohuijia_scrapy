#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-16 14:42:12
# Project: skykiwichina
from lxml import etree
from pyspider.libs.base_handler import *
from mysql_conf import ToMysql
import time

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://news.skykiwichina.com', callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):
        content=response.content
        tree=etree.HTML(content)
        urls = tree.xpath("//div[@id='m_left']//a/@href")
        for url in urls:
            if "shtml" in url:
                self.crawl(url, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        images = tree.xpath("//div[@class='artText']//img/@src")
        index = 0
        for i in images:
            if 'http' not in i:
                images[index] = "http://news.skykiwichina.com" + i
            else:
                images[index] = i
            index += 1
        article_time = tree.xpath("//h5/text()")
        title = tree.xpath("//h1/text()")
        text = tree.xpath("//div[@class='artText']//p/text()")
        sql = ToMysql()
        data = {
            "title": "".join(title),
            "text": "".join(text),
            "article_time": article_time[0][-23:-4].encode("utf8"),
            "spider_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "image_1": images[0] if len(images) >= 1 else None,
            "image_2": images[1] if len(images) >= 2 else None,
            "image_3": images[2] if len(images) >= 3 else None,
            "source": "skykiwichina",
            "tab": 0,
        }
        sql.into(**data)
        return data
