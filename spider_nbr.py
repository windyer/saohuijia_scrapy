#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-01-03 14:01:30
# Project: nbr

from pyspider.libs.base_handler import *
from lxml import etree
from mysql_conf import ToMysql
import datetime
from bs4 import BeautifulSoup
from mysql_conf import FormatContent


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=12 * 60)
    def on_start(self):
        page =3
        for i in range(page):
            self.crawl('https://www.nbr.co.nz/search/site/china?page={0}'.format(str(i+1)), callback=self.index_page)
            self.crawl('https://www.nbr.co.nz/search/site/chinese?page={0}'.format(str(i+1)), callback=self.index_page)

    @config(age=12* 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if "article" in each.attr.href:
                self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        title = tree.xpath("//h1[@class='page-title']/text()")
        article_time = tree.xpath("//span[@class='meta meta-date']/text()")
        images = tree.xpath("//img[@class='rsImg rsMainSlideImage']/@src")
        soup = BeautifulSoup(content)
        text = soup.select('div[class="field-items"]')
        content = str(text[1])
        sql = ToMysql()
        format_content = FormatContent()
        data = {
            "Title": "".join(title),
            "Content":format_content.format_content(str(content)),
            "AddTime":str(datetime.datetime.strptime(article_time[0],'%A %B %d, %Y'))[:10],
            "Images": ",".join(images),
            "ImageNum": len(images),
            "Language": 0,
            "NewsSource": "nbr",
            "Link": response.url
        }
        #try:
        #    sql.into(**data)
        #except:
        #    raise
        return data
