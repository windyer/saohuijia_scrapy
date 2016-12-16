#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-16 14:42:12
# Project: skykiwichina
from lxml import etree
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://news.skykiwichina.com', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
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
        image = tree.xpath("//div[@class='artText']//img/@src")
        index = 0
        for i in image:
            image[index] = "'http://news.skykiwichina.com'" + i
            index += 1
        time = tree.xpath("//h5/text()")
        title = tree.xpath("//h1/text()")
        text = tree.xpath("//div[@class='artText']//p/text()")
        return {
            "title": title[0].encode("utf8"),
            "image":image,
            "time":time[0][-23:-4].encode("utf8"),
            "text":"".join(text),
        }
