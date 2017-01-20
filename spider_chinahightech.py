#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-01-18 16:21:17
# Project: chinahightech

import json
from newspaper import Article
from pyspider.libs.base_handler import *
from lxml import etree
from mysql_conf import ToMysql
import datetime
from bs4 import BeautifulSoup
from mysql_conf import FormatContent
from qiniu_update import update
import timer

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        #if not timer.timer():
        #    return
        self.crawl('http://storage.chinahightech.com/index.php?class=1&m=search&c=index&a=search_k&typeid=&siteid=1&q=%D0%C2%CE%F7%C0%BC', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if '.html' in each.attr.href:
                self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        title = tree.xpath("//h1/text()")
        article_time = tree.xpath("//div[@class='addtime']/text()")
        images = tree.xpath("//div[@class='content']//img/@src")
        soup = BeautifulSoup(content)
        text = soup.select('div[class="content"]')
        content = str(text[0])
        soup2 = BeautifulSoup(content)
        s=[s.extract() for s in soup2('script')]
        s=[s.extract() for s in soup2('style')]
        image_tap =soup2.select('img')
        content2 = str(soup2)
        images2 = []
        for image,tap in zip(images,image_tap):
            if image != '':
                new_image = update.load(image, "chinahightech")
                images2.append(new_image)
                content = content.replace(image,new_image)
                content2 = content2.replace(str(tap),"(url,"+str(new_image)+")")
        text = ''.join(BeautifulSoup(content2).findAll(text=True))
        sql = ToMysql()
        format_content = FormatContent()
        data = {
            "Title": "".join(title).replace("\n","").replace("\r","").replace("\t",""),
            "Content":format_content.format_content(str(content)),
            "AddTime":article_time[0].replace("\n","").replace("\r",""),
            "Images": ",".join(images2),
            "ImageNum": len(images2),
            "Language": 0,
            "NewsSource": "高新网",
            "Link": response.url,
            "PlainText":text,

        }
        #try:
        #    sql.into(**data)
        #except:
        #    raise
        return data