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
from qiniu_update import update
import timer
class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes= 60)
    def on_start(self):
        #if not timer.timer():
        #    return
        self.crawl('http://news.skykiwichina.com', callback=self.index_page)

    @config(age=10*24*60 * 60)
    def index_page(self, response):
        content=response.content
        tree=etree.HTML(content)
        urls = tree.xpath("//div[@id='m_left']//a/@href")
        for url in urls:
            if "shtml" in url and "skyk" in url:
                self.crawl(url, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        content = response.content
        tree = etree.HTML(content)

        article_time = tree.xpath("//h5/text()")
        title = tree.xpath("//h1/text()")
        soup = BeautifulSoup(response.content)
        text=soup.select('div[class="artText"]')
        content = str(text[0])
        images = tree.xpath("//div[@class='artText']//img/@src")
        soup2 = BeautifulSoup(content)
        #s=[s.extract() for s in soup2('span')]
        image_tap =soup2.select('img')
        content2 = str(soup2)
        index = 0
        images2=[]
        for i,tap in zip(images,image_tap):
            if 'http' not in i:
                new_image = update.load("http://news.skykiwichina.com" + i, "skykiwichina")
                images2.append(new_image)
                content = content.replace(i, new_image)
                content2 = content2.replace(str(tap),"(url,"+str(new_image)+")")
            else:
                new_image = update.load(i, "skykiwichina")
                images2.append(new_image)
                content = content.replace(i, new_image)
                content2 = content2.replace(str(tap),"(url,"+str(new_image)+")")
            index += 1
        text = ''.join(BeautifulSoup(content2).findAll(text=True))
        sql = ToMysql()
        format_content = FormatContent()
        data = {
            "Title": "".join(title),
            "Content": format_content.format_content(content),
            "AddTime": article_time[0][-23:-4].encode("utf8"),
            "Images": ",".join(images2),
            "ImageNum":len(images2),
            "Language": 1,
            "NewsSource": "新西兰天维网站",
            "Link":response.url,
            "PlainText":text,

        }
        #sql.into(**data)
        return data
