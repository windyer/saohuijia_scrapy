#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-01-04 15:09:13
# Project: finance_sina

from pyspider.libs.base_handler import *
from pyspider.libs.base_handler import *
from lxml import etree
from mysql_conf import ToMysql
import datetime
from bs4 import BeautifulSoup
from mysql_conf import FormatContent


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://search.sina.com.cn/?country=usstock&q=%E6%96%B0%E8%A5%BF%E5%85%B0&name=%E6%96%B0%E8%A5%BF%E5%85%B0&t=&c=news&k=%E6%96%B0%E8%A5%BF%E5%85%B0&range=all&col=1_7&from=channel&ie=utf-8', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if "shtml" in each.attr.href:
                self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        title = tree.xpath("//h1/text()")
        article_time = tree.xpath("//span[@id='pub_date']/text()")
        if len(article_time)==0:
            article_time = tree.xpath("//span[@class='time-source']/text()")
        images = tree.xpath("//div[@id='artibody']//div//img/@src")
        soup = BeautifulSoup(content)
        text = soup.select('div[id="artibody"]')
        content = str(text[0])
        soup2 = BeautifulSoup(content)
        s=soup2.select('div')
        sql = ToMysql()
        format_content = FormatContent()
        data = {
            "Title": "".join(title).replace("\n","").replace("\r",""),
            "Content":s[1],#format_content.format_content(str(s)),
            "AddTime":article_time[0].strip().replace("\n","").replace(u"年","-").replace(u"月","-").replace(u"日"," ").encode("utf8"),
            "Images": ",".join(images),
            "ImageNum": len(images),
            "Language": 0,
            "NewsSource": "新浪财经",
            "Link": response.url
        }
        #try:
        #    sql.into(**data)
        #except:
        #    raise
        return data