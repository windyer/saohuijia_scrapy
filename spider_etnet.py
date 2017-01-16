#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-01-11 16:56:03
# Project: etnet

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
        self.crawl('http://news.baidu.com/ns?cl=2&rn=20&tn=news&word=site%3Anews.etnet.com.cn', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if "htm" in each.attr.href and "etnet" in each.attr.href:
                self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        title = tree.xpath("//span[@class='globalTextWord ']/text()")
        article_time = tree.xpath("//span[@class='featureTime']/text()")
        images = tree.xpath("//div[@class='Newstextall']//img/@src")
        soup = BeautifulSoup(content)
        text = soup.select('div[class="Newstextall"]')
        content = str(text[0])
        images2 = []
        for image in images:
            if image != '':
                new_image = update.load(image, "etnet")
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
            "NewsSource": "经济通",
            "Link": response.url
        }
        #try:
        #    sql.into(**data)
        #except:
        #    raise
        return data