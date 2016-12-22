#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-16 16:43:58
# Project: chinaconsulate
from newspaper import Article
from pyspider.libs.base_handler import *
from lxml import etree
from mysql_conf import ToMysql
import time
from bs4 import BeautifulSoup
from mysql_conf import FormatContent

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.chinaconsulate.org.nz/chn/xwdt/', callback=self.index_page)

    @config(age=60 * 60)
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
        article_time = tree.xpath("//div[@id='News_Body_Time']/text()")
        images = article.images
        soup = BeautifulSoup(response.content)
        text = soup.select('div[id="News_Body_Txt_A"]')
        content = str(text[0])
        soup2 = BeautifulSoup(content)
        imgs =soup2.select('img')
        for img,img2 in zip(imgs,images):
            content=content.replace(img['src'],img2.encode("utf8"))
        sql = ToMysql()
        format_content = FormatContent()
        data = {
            "Title": article.title,
            "Content": format_content.format_content(content),
            "AddTime": article_time[0],
            "Images": ",".join(images),
            "ImageNum": len(images),
            "Language": 1,
            "NewsSource": "驻奥克兰总领馆",
            "Link": response.url
        }
        #try:
            #sql.into(**data)
        #except:
            #raise
        return data