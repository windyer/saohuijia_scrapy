#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-01-18 20:10:25
# Project: cqn

from pyspider.libs.base_handler import *
from lxml import etree
from mysql_conf import ToMysql
import datetime
from bs4 import BeautifulSoup, Comment
from mysql_conf import FormatContent
from qiniu_update import update
import timer
import re
class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://news.baidu.com/ns?ct=0&rn=20&ie=utf-8&bs=%E6%96%B0%E8%A5%BF%E5%85%B0+site%3Acqn.com.cn&rsv_bp=1&sr=0&cl=2&f=8&prevct=no&tn=news&word=%E6%96%B0%E8%A5%BF%E5%85%B0+site%3Acqn.com.cn&inputT=20376', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if "htm" in each.attr.href and "cqn" in each.attr.href:
                self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        title = tree.xpath("//h1/text()")
        article_time = tree.xpath("//div[@class='publish']/text()")
        images = tree.xpath("//div[@class='content']//img/@src")
        soup = BeautifulSoup(content)
        text = soup.select('div[class="content"]')
        content = str(text[0])
        soup2 = BeautifulSoup(content)
        #s=[s.extract() for s in soup2('style')]
        image_tap =soup2.select('img')
        comments = soup2.findAll(text=lambda text:isinstance(text, Comment))
        [comment.extract() for comment in comments]
        content2 = str(soup2)
        images2 = []
        for image,tap in zip(images,image_tap):
            if image != '':
                new_image = update.load(image, "cqn")
                images2.append(new_image)
                content = content.replace(image,new_image)
                content2 = content2.replace(str(tap),"(url,"+str(new_image)+")")
        text = ''.join(BeautifulSoup(content2).findAll(text=True))

        sql = ToMysql()
        format_content = FormatContent()
        data = {
            "Title": "".join(title),
            "Content":format_content.format_content(str(content)),
            "AddTime":"".join(article_time),
            "Images": ",".join(images2),
            "ImageNum": len(images2),
            "Language": 0,
            "NewsSource": "中国质量新闻网",
            "Link": response.url,
            "PlainText":text,

        }
        #try:
        #    sql.into(**data)
        #except:
        #    raise
        return data
