#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-01-11 16:56:03
# Project: stockstar

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
        self.crawl('http://news.baidu.com/ns?word=site%3Ajrj.com.cn&tn=news&from=news&cl=2&rn=50&ct=1', callback=self.index_page)

    @config(age=10*6* 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if "shtml" in each.attr.href and "jrj" in each.attr.href and "fund" not in each.attr.href:
                self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        title = tree.xpath("//h1/text()")
        article_time = tree.xpath("//p[@class='inftop']//span/text()")
        images = tree.xpath("//div[@class='texttit_m1']//img/@src")
        soup = BeautifulSoup(content)
        text = soup.select('div[class="texttit_m1"]')
        content = str(text[0])
        soup2 = BeautifulSoup(content)
        s=[s.extract() for s in soup2('script')]
        s=[s.extract() for s in soup2('style')]
        image_tap =soup2.select('img')
        content2 = str(soup2)
        images2 = []
        for image,tap in zip(images,image_tap):
            if image != '':
                new_image = update.load(image, "jrj")
                images2.append(new_image)
                content = content.replace(image,new_image)
                content2 = content2.replace(str(tap),"(url,"+str(new_image)+")")
        text = ''.join(BeautifulSoup(content2).findAll(text=True))
        sql = ToMysql()
        format_content = FormatContent()
        data = {
            "Title": "".join(title).replace("\n","").replace("\r","").replace("\t",""),
            "Content":format_content.format_content(str(content)),
            "AddTime":article_time[0].replace("\n","").replace("\r",""),
            "Images": ",".join(images2),
            "ImageNum": len(images2),
            "Language": 0,
            "NewsSource": "金融界",
            "Link": response.url,
            "PlainText":text,

        }
        #try:
        #    sql.into(**data)
        #except:
        #    raise
        return data