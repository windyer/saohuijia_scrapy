#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-01-03 15:18:01
# Project: govt

from pyspider.libs.base_handler import *
from pyspider.libs.base_handler import *
from lxml import etree
from mysql_conf import ToMysql
import datetime
from bs4 import BeautifulSoup
from mysql_conf import FormatContent
import urllib
from qiniu_update import update
import timer
class Handler(BaseHandler):
    crawl_config = {
    }
    def __init__(self):
        self.page = 20
        self.china = "https://enz.govt.nz/home/SearchForm?Search=china&start={0}"
        self.chinese = "https://enz.govt.nz/home/SearchForm?Search=chinese&start={0}"

    @every(minutes=60)
    def on_start(self):
        #if not timer.timer():
        #    return
        for i in range(self.page):
            self.crawl(self.china.format(str(i*10)), callback=self.index_page,validate_cert=False)
            self.crawl(self.chinese.format(str(i*10)), callback=self.index_page,validate_cert=False)

    @config(age=24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if "ed-news" in each.attr.href:
                self.crawl(each.attr.href, callback=self.detail_page,validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        title = tree.xpath("//h1/text()")
        article_time = tree.xpath("//div[@class='col-xs-12 col-sm-3 date']//p/text()")
        soup = BeautifulSoup(content)
        text = soup.select('div[class="article"]')
        content = str(text[0])
        tree = etree.HTML(content)
        images = tree.xpath("//img/@src")
        soup2 = BeautifulSoup(content)
        s=[s.extract() for s in soup2('span')]
        image_tap =soup2.select('img')
        content2 = str(soup2)
        content = str(soup2)
        images2=[]
        for image,tap in zip(images,image_tap):
            if image != '' and 'http' not in image:
                new_image = update.load("https://enz.govt.nz/"+image, "govt")
                images2.append(new_image)
                content = content.replace(image,new_image)
                content2 = content2.replace(str(tap),"(url,"+str(new_image)+")")
        text = ''.join(BeautifulSoup(content2).findAll(text=True))
        sql = ToMysql()
        format_content = FormatContent()
        data = {
            "Title": "".join(title),
            "Content":format_content.format_content(content),
            "AddTime":str(datetime.datetime.strptime(article_time[0],'%d %B %Y'))[:10],
            "Images": ",".join(images2),
            "ImageNum": len(images),
            "Language": 0,
            "NewsSource": "govt",
            "Link": response.url,
            "PlainText":text,

        }
        #try:
        #    sql.into(**data)
        #except:
        #    raise
        return data