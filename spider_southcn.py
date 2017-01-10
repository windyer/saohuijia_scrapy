#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-01-03 16:23:58
# Project: southcn

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
        count = 20
        self.crawl('http://search.southcn.com/web/search?channelid=216505&searchword=%E6%96%B0%E8%A5%BF%E5%85%B0&perpage={0}'.format(str(count)), callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if "content" in each.attr.href:
                self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        title = tree.xpath("//h2[@id='article_title']/text()")
        article_time = tree.xpath("//span[@class='pub_time']/text()")
        images = tree.xpath("//div[@class='content']//img/@src")
        soup = BeautifulSoup(content)
        text = soup.select('div[class="content"]')
        content = str(text[0])
        sql = ToMysql()
        format_content = FormatContent()
        data = {
            "Title": "".join(title),
            "Content":format_content.format_content(str(content)),
            "AddTime":"".join(article_time),
            "Images": ",".join(images),
            "ImageNum": len(images),
            "Language": 0,
            "NewsSource": "南方新闻",
            "Link": response.url
        }
        #try:
        #    sql.into(**data)
        #except:
        #    raise
        return data