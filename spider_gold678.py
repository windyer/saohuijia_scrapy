#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-01-11 18:09:14
# Project: gold678

from pyspider.libs.base_handler import *
from newspaper import Article
from lxml import etree
from mysql_conf import ToMysql
import time
from bs4 import BeautifulSoup
from mysql_conf import FormatContent
from qiniu_update import update
import timer

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=60)
    def on_start(self):
        if not timer.timer():
            return
        self.crawl('http://www.gold678.com/dy/Search/%E6%96%B0%E8%A5%BF%E5%85%B0', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if "html" in each.attr.href and "C" in each.attr.href:
                self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        title = tree.xpath("//h1/text()")
        article_time = tree.xpath("//span[@class='time_font']/text()")
        images = tree.xpath("//div[@class='news_inter_area']//img/@src")
        soup = BeautifulSoup(content)
        text = soup.select('div[class="news_inter_area"]')
        content = str(text[0])
        images2 = []
        for image in images:
            if image != '':
                new_image = update.load(image, "gold678")
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
            "NewsSource": "汇金网",
            "Link": response.url
        }
        #try:
        #    sql.into(**data)
        #except:
        #    raise
        return data