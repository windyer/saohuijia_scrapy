#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-01-18 20:36:09
# Project: westpac

from lxml import etree
from pyspider.libs.base_handler import *
from mysql_conf import ToMysql
import time
from bs4 import BeautifulSoup
from mysql_conf import FormatContent
from qiniu_update import update
import timer
import datetime

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.westpac.co.nz/rednews/community', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        content=response.content
        tree=etree.HTML(content)
        urls = tree.xpath("//h2[@class='rn-summary__title rn-h5']//a/@href")
        for i in urls:
            self.crawl("https://www.westpac.co.nz"+i, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        title = tree.xpath("//h1/text()")
        article_time = tree.xpath("//time[@class='rn-posted']/text()")
        soup = BeautifulSoup(response.content)
        text = soup.select('section[class="entry-content"]')
        content = str(text[0])
        images = tree.xpath("//section[@class='entry-content']//img/@src")
        soup2 = BeautifulSoup(content)
        #s=[s.extract() for s in soup2('section')]
        #s=[s.extract() for s in soup2('script')]
        image_tap =soup2.select('img')
        content2 = str(soup2)
        images2=[]
        for image,tap in zip(images,image_tap):
            if image != '':
                #new_image = update.load(image, "westpac")
                #images2.append(new_image)
                content = content.replace(image,"https://www.westpac.co.nz/"+image)
                content2 = content2.replace(str(tap),"(url,"+str("https://www.westpac.co.nz/"+image)+")")
        text = ''.join(BeautifulSoup(content2).findAll(text=True))
        #imgs = soup2.select('img')
        #for img, img2 in zip(imgs, images2):
        #    content = content.replace(img['src'], img2.encode("utf8"))
        sql = ToMysql()
        format_content = FormatContent()
        t = "".join(article_time)
        #for i in self.moon.keys():
        #    if i in t:
        #        t = t.replace(i,self.moon[i])
        data = {
            "Title": "".join(title),
            "Content": format_content.format_content(str(content)),
            "AddTime": str(datetime.datetime.strptime(article_time[0][7:],'%d %B %Y'))[:10],
            "Images": ",".join(images2),
            "ImageNum": len(images2),
            "Language": 0,
            "NewsSource": "westpac",
            "Link": response.url,
            "PlainText":text,

        }
        #try:
        #    sql.into(**data)
        #except:
         #   raise
        return data
