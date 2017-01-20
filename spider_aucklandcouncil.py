#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-26 10:31:19
# Project: aucklandcouncil

from pyspider.libs.base_handler import *
from newspaper import Article
from lxml import etree
from mysql_conf import ToMysql
import time
from bs4 import BeautifulSoup
from mysql_conf import FormatContent
import datetime
from qiniu_update import update
import timer
import re
class Handler(BaseHandler):
    crawl_config = {
    }
    def __init__(self):
        self.page = 4
        self.url = 'http://ourauckland.aucklandcouncil.govt.nz/search?k=china&s=0&p={0}'
        self.url2 = 'http://ourauckland.aucklandcouncil.govt.nz/search?k=chinese&s=0&p={0}'
    @every(minutes=60)
    def on_start(self):
        #if not timer.timer():
        #    return
        urls=[]
        for i in range(self.page):
            urls.append(self.url.format(str(i)))
            urls.append(self.url2.format(str(i)))
        self.crawl(urls, callback=self.index_page)

    @config(age=12 *60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if 'article' in each.attr.href:
                self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        url = response.url
        article = Article(url)
        article.download()
        article.parse()
        tree = etree.HTML(response.content)
        article_time = tree.xpath("//span[@class='uk-float-left ns-published']/text()")
        images = tree.xpath("//div[@class='ns-hero']//a/@href")
        soup = BeautifulSoup(response.content)
        #head = soup.select('div[class="ns-hero"]')
        text = soup.select('div[class="ns-single-page-content"]')
        images2 = []
        content = str(text[0])
        for image in images:
            if image != '' and 'http' not in image:
                new_image = update.load("http://ourauckland.aucklandcouncil.govt.nz" + image, "aucklandcouncil")
                content = content.replace(image, new_image)
                images2.append(new_image)

        sql = ToMysql()
        dr = re.compile(r'<[^>]+>', re.S)
        text = dr.sub('', content)
        if len(images2) >0:
            content = "<img src={0}>".format(images2[0])+content
            content2 = "(url,{0})".format(images2[0])+content
            text = dr.sub('', content2)


        format_content = FormatContent()
        t = "".join(article_time)
        data = {
            "Title": article.title,
            "Content": format_content.format_content(content),
            "AddTime": str(datetime.datetime.strptime(t,' %d %B %Y'))[:10],
            "Images": ",".join(images2),
            "ImageNum": len(images2),
            "Language": 0,
            "NewsSource": "奥克兰市政府",
            "Link": response.url,
            "PlainText":text,
        }
        #try:
        #    sql.into(**data)
       # except:
         #   raise
        return data

