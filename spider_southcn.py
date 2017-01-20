#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-01-03 16:23:58
# Project: southcn

from pyspider.libs.base_handler import *
from lxml import etree
from mysql_conf import ToMysql
import datetime
from bs4 import BeautifulSoup, Comment
from mysql_conf import FormatContent
from qiniu_update import update
import timer
import re
class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=60)
    def on_start(self):
        #if not timer.timer():
        #    return
        count = 20
        self.crawl('http://search.southcn.com/web/search?channelid=216505&searchword=%E6%96%B0%E8%A5%BF%E5%85%B0&perpage={0}'.format(str(count)), callback=self.index_page)

    @config(age=10*24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if "content" in each.attr.href:
                self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        title = tree.xpath("//h2[@id='article_title']/text()")
        article_time = tree.xpath("//span[@class='pub_time']/text()")
        images = tree.xpath("//div[@class='content']//img/@src")
        soup = BeautifulSoup(content)
        text = soup.select('div[class="content"]')
        content = str(text[0])
        soup2 = BeautifulSoup(content)
        #s=[s.extract() for s in soup2('style')]
        image_tap =soup2.select('img')
        comments = soup2.findAll(text=lambda text:isinstance(text, Comment))
        [comment.extract() for comment in comments]
        content2 = str(soup2)
        images2 = []
        for image,tap in zip(images,image_tap):
            if image != '':
                new_image = update.load(image, "southcn")
                images2.append(new_image)
                content = content.replace(image,new_image)
                content2 = content2.replace(str(tap),"(url,"+str(new_image)+")")
        dr = re.compile(r'<[^>]+>', re.S)
        text = dr.sub('', content2)
        sql = ToMysql()
        format_content = FormatContent()
        data = {
            "Title": "".join(title),
            "Content":format_content.format_content(str(content)),
            "AddTime":"".join(article_time),
            "Images": ",".join(images2),
            "ImageNum": len(images2),
            "Language": 0,
            "NewsSource": "南方新闻",
            "Link": response.url,
            "PlainText":text,

        }
        #try:
        #    sql.into(**data)
        #except:
        #    raise
        return data
