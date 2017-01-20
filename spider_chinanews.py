#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-01-03 16:45:44
# Project: chinanews
from pyspider.libs.base_handler import *
from lxml import etree
from mysql_conf import ToMysql
import datetime
from bs4 import BeautifulSoup
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
        self.crawl('http://sou.chinanews.com.cn/search.do?q=%E6%96%B0%E8%A5%BF%E5%85%B0', callback=self.index_page)

    @config(age=6*60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if "shtml" in each.attr.href:
                self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        title = tree.xpath("//h1/text()")
        article_time = tree.xpath("//div[@class='left-t']/text()")
        images = tree.xpath("//div[@class='left_zw']//img/@src")
        soup = BeautifulSoup(content)
        text = soup.select('div[class="left_zw"]')
        content = str(text[0])

        soup2 = BeautifulSoup(content)
        s=[s.extract() for s in soup2('table')]
        image_tap = soup2.select('img')
        images2=[]
        content2 = str(soup2)
        content = str(soup2)
        for image,tap in zip(images,image_tap):
            if image != '':
                new_image = update.load(image, "chinanews")
                images2.append(new_image)
                content = content.replace(image,new_image)
                content2 = content2.replace(str(tap),"(url,"+str(new_image)+")")
        sql = ToMysql()
        format_content = FormatContent()
        #dr = re.compile(r'<[^>]+>', re.S)
        #text = dr.sub('', content2)
        text = ''.join(BeautifulSoup(content2).findAll(text=True))
        data = {
            "Title": "".join(title).replace("\n","").replace("\r",""),
            "Content":format_content.format_content(str(content)),
            "AddTime":article_time[0][1:18].replace(u"年","-").replace(u"月","-").replace(u"日","").encode("utf8"),
            "Images": ",".join(images2),
            "ImageNum": len(images2),
            "Language": 0,
            "NewsSource": "中国新闻网",
            "Link": response.url,
            "PlainText":text,
        }
        #try:
        #    sql.into(**data)
        #except:
        #    raise
        return data
