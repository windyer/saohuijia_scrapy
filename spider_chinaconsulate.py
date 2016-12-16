#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-16 16:43:58
# Project: chinaembassy
from newspaper import Article
from pyspider.libs.base_handler import *
from lxml import etree


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.chinaembassy.org.nz/chn/', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
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
        time = tree.xpath("//div[@id='News_Body_Time']/text()")
        return {
            "title": article.title,
            "text":article.text,
            "image":article.images,
            "time":time[0]
        }
