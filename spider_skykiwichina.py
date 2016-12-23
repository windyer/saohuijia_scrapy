#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-16 14:42:12
# Project: skykiwichina
from lxml import etree
from pyspider.libs.base_handler import *
from mysql_conf import ToMysql
import time
from bs4 import BeautifulSoup
from mysql_conf import FormatContent

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://news.skykiwichina.com', callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):
        content=response.content
        tree=etree.HTML(content)
        urls = tree.xpath("//div[@id='m_left']//a/@href")
        for url in urls:
            if "shtml" in url and "skykiwichina" in url:
                self.crawl(url, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        images = tree.xpath("//div[@class='artText']//img/@src")
        index = 0
        for i in images:
            if 'http' not in i:
                images[index] = "http://news.skykiwichina.com" + i
            else:
                images[index] = i
            index += 1
        article_time = tree.xpath("//h5/text()")
        title = tree.xpath("//h1/text()")
        soup = BeautifulSoup(response.content)
        text=soup.select('div[class="artText"]')
        images2=[]
        content = str(text[0])
        sql = ToMysql()
        format_content = FormatContent()
        data = {
            "Title": "".join(title),
            "Content": format_content.format_content(content),
            "AddTime": article_time[0][-23:-4].encode("utf8"),
            "Images": ",".join(images),
            "ImageNum":len(images),
            "Language": 1,
            "NewsSource": "新西兰天维网站",
            "Link":response.url
        }
        #sql.into(**data)
        return data
