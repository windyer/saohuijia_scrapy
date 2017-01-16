#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-15 16:42:02
# Project: jiemian

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
    def __init__(self):
        self.page = 50

    @every(minutes=60)
    def on_start(self):
        if not timer.timer():
            return
        urls=[]
        url="http://a.jiemian.com/index.php?m=search&a=index&msg=%E6%96%B0%E8%A5%BF%E5%85%B0&type=news&page={}"
        for i in range(self.page):
            urls.append(url.format(str(i+1)))
        self.crawl(urls, callback=self.index_page)

    @config(age=12*60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if 'jiemian' in each.attr.href:
                detail_url = each.attr.href
                if ("article" in detail_url) and ("html" in detail_url):
                    self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        url = response.url
        article=Article(url,language='zh')
        article.download()
        article.parse()
        tree = etree.HTML(response.content)
        article_time = tree.xpath("//span[@class='date']/text()")
        images = tree.xpath("//div[@class='article-main']//img/@src")
        soup = BeautifulSoup(response.content)
        text=soup.select('div[class="article-content"]')
        images2=[]
        content = str(text[0])
        for image in images:
            if image !='' and 'http'not in image:
                new_image = update.load("http:"+image, "jiemian")
                images2.append(new_image)
                content=content.replace(image,new_image)
        sql = ToMysql()
        format_content = FormatContent()
        data = {
            "Title": article.title,
            "Content": format_content.format_content(content),
            "AddTime": article_time[0].replace("/","-"),
            "Images": ",".join(images2),
            "ImageNum":len(images),
            "Language": 1,
            "NewsSource": "界面",
            "Link":response.url
        }
        #try:
        #    sql.into(**data)
        #except:
        #    raise
        return data

