#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-01-11 16:56:03
# Project: stockstar

from pyspider.libs.base_handler import *
from newspaper import Article
from lxml import etree
from mysql_conf import ToMysql
import time
from bs4 import BeautifulSoup
from mysql_conf import FormatContent
from qiniu_update import update


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://news.baidu.com/ns?word=site%3Astockstar.com&tn=news&from=news&cl=2&rn=20&ct=1', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if "shtml" in each.attr.href and "stocksta" in each.attr.href:
                self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        title = tree.xpath("//h1/text()")
        article_time = tree.xpath("//span[@id='pubtime_baidu']/text()")
        images = tree.xpath("//div[@class='article']//img/@src")
        soup = BeautifulSoup(content)
        text = soup.select('div[class="article"]')
        content = str(text[0])
        images2 = []
        for image in images:
            if image != '':
                new_image = update.load(image, "stocksta")
                images2.append(new_image)
                content = content.replace(image, new_image)
        sql = ToMysql()
        format_content = FormatContent()
        data = {
            "Title": "".join(title),
            "Content":format_content.format_content(str(content)),
            "AddTime":"".join(article_time),
            "Images": ",".join(images2),
            "ImageNum": len(images2),
            "Language": 0,
            "NewsSource": "证券之星",
            "Link": response.url
        }
        #try:
        #    sql.into(**data)
        #except:
        #    raise
        return data