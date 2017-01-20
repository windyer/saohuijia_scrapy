#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-15 15:22:33
# Project: fmprc

from pyspider.libs.base_handler import *
from newspaper import Article
from lxml import etree
from mysql_conf import ToMysql
import time
from bs4 import BeautifulSoup
from mysql_conf import FormatContent
from qiniu_update import update
import timer
class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=60)
    def on_start(self):
        #if not timer.timer():
        #    return
        self.crawl('http://www.fmprc.gov.cn/wjb/web_search.jsp?presearchword=&channelid=75003&siteid=5243&prepage=500&page=1&searchword=%E6%96%B0%E8%A5%BF%E5%85%B0+and+siteid%3D5243&sw=%E6%96%B0%E8%A5%BF%E5%85%B0&select=1', callback=self.index_page)

    @config(age=24*60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            detail_url=each.attr.href
            if "html" in detail_url and 'fmprc' in detail_url:
                self.crawl(detail_url, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        url = response.url
        article=Article(url,language='zh')
        article.download()
        article.parse()
        tree = etree.HTML(response.content)
        article_time = tree.xpath("//span[@id='News_Body_Time']/text()")
        images= []
        for image in article.images:
            if "jpg" in image:
                images.append(image)
        soup = BeautifulSoup(response.content)
        text = soup.select('div[id="News_Body_Txt_A"]')
        content = str(text[0])
        soup2 = BeautifulSoup(content)
        imgs =soup2.select('img')
        images2=[]
        content2 = str(soup2)
        for img,img2 in zip(imgs,images):
            new_image = update.load(img2.encode("utf8"), "fmprc")
            images2.append(new_image)
            content2 = content2.replace(str(img),"(url,"+str(img2)+")")
            content=content.replace(img['src'],new_image)
        text = ''.join(BeautifulSoup(content2).findAll(text=True))
        sql = ToMysql()
        format_content = FormatContent()
        data = {
            "Title": article.title,
            "Content": format_content.format_content(content),
            "AddTime": article_time[0],
            "Images": ",".join(images2),
            "ImageNum": len(images2),
            "Language": 1,
            "NewsSource": "驻奥克兰总领馆",
            "Link": response.url,
            "PlainText":text,
        }
        #try:
        #    sql.into(**data)
        #except:
        #    raise
        return data

