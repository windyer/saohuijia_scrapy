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
from qiniu_update import update
import timer

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=60)
    def on_start(self):
        #if not timer.timer():
        #    return
        page =2
        for i in range(page):
            self.crawl('https://www.nbr.co.nz/search/site/china?page={0}'.format(str(i+1)), callback=self.index_page)
            self.crawl('https://www.nbr.co.nz/search/site/chinese?page={0}'.format(str(i+1)), callback=self.index_page)

    @config(age=10*12* 60 * 60)
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
        images2=[]
        soup2 = BeautifulSoup(content)
        #s=[s.extract() for s in soup2('span')]
        image_tap =soup2.select('img')
        content2 = str(soup2)
        for image,tap in zip(images,image_tap):
            if image != '':
                new_image = update.load(image, "nbr")
                images2.append(new_image)
                content = content.replace(image,new_image)
                content2 = content2.replace(str(tap),"(url,"+str(new_image)+")")
        text = ''.join(BeautifulSoup(content2).findAll(text=True))
        sql = ToMysql()
        format_content = FormatContent()
        data = {
            "Title": "".join(title),
            "Content":format_content.format_content(str(content)),
            "AddTime":str(datetime.datetime.strptime(article_time[0],'%A %B %d, %Y'))[:10],
            "Images": ",".join(images2),
            "ImageNum": len(images2),
            "Language": 0,
            "NewsSource": "nbr",
            "Link": response.url,
            "PlainText":text,

        }
        #try:
        #    sql.into(**data)
        #except:
        #    raise
        return data
