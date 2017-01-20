#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-19 10:06:22
# Project: kannz
from lxml import etree
from pyspider.libs.base_handler import *
from mysql_conf import ToMysql
import time
from bs4 import BeautifulSoup
from mysql_conf import FormatContent
from qiniu_update import update
import timer

class Handler(BaseHandler):
    crawl_config = {
    }
    def __init__(self):
        self.page_cout = 10
        self.url = "http://www.kannz.com/page/{0}/"
    @every(minutes=60)
    def on_start(self):
        #if not timer.timer():
        #    return
        for page in range(self.page_cout):
            url = self.url.format(str(page+1))
            self.crawl(url, callback=self.index_page)

    @config(age=10*12*60 * 60)
    def index_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        urls = tree.xpath("//article[@class='excerpt']//header//h2//a/@href")
        urls2 = []
        for i in urls:
            if "kannz" in i:
                urls2.append(i)
        self.crawl(urls2, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        tree = etree.HTML(response.content)
        article_time = tree.xpath("//time[@class='muted']/text()")
        #txt = tree.xpath("//p/text()")
        title = tree.xpath("//h1[@class='article-title']//a/text()")
        images = tree.xpath("//article[@class='article-content']//img/@src")
        soup = BeautifulSoup(response.content)
        text=soup.select('article[class="article-content"]')
        images2=[]
        content = str(text[0])
        soup2 = BeautifulSoup(content)
        s=[s.extract() for s in soup2('span')]
        image_tap =soup2.select('img')
        content2 = str(soup2)
        for image,tap in zip(images,image_tap):
            if image != '':
                content2 = content2.replace(str(tap),"(url,"+str(image)+")")
        text = ''.join(BeautifulSoup(content2).findAll(text=True))
        sql = ToMysql()
        format_content = FormatContent()
        data = {
            "Title": "".join(title),
            "Content": format_content.format_content(content),
            "AddTime": article_time[0],
            "Images": ",".join(images),
            "ImageNum":len(images),
            "Language": 1,
            "NewsSource": "看新西兰",
            "Link":response.url,
            "PlainText":text,

        }
        #try:
        #    sql.into(**data)
        #except:
        #    raise
        return data

