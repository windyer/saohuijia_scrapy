#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-17 11:50:37
# Project: weibo

from pyspider.libs.base_handler import *
from lxml import etree
from newspaper import Article
import re
from mysql_conf import ToMysql
import time
from bs4 import BeautifulSoup
from mysql_conf import FormatContent
import timer
class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.page_count = 10
        self.urls = "http://weibo.cn/purenewzealand?page={0}&vt=4"

        self.cookie = {
            "SUB": "_2A251WJemDeRxGeBO7loR9izPyDiIHXVWojnurDV6PUJbkdANLVn_kW0Su3tWX5A572aPZpCVIGW8rjvpZA..",
            "_T_WM": "726bd3559528a46dbebb09c261a63991",
            "gsid_CTandWM": "4uCbe0e41uI7DZkYaE2k5ppYG5o",
        }

    @every(minutes=60)
    def on_start(self):
        #if not timer.timer():
        #    return
        for page in range(self.page_count):
            url = self.urls.format(str(page+1))
            self.crawl(url, callback=self.index_page, cookies=self.cookie)

    @config(age=12*10*60 * 60)
    def index_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        urls = tree.xpath("//div[@class='c']//a/@href")
        urls2 = []
        for i in urls:
            if "sinaurl" in i:
                print i
                urls2.append(i)
        self.crawl(urls2, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        if "weixin" in response.url:
            link_list = re.findall(r'(?<=URL\=).+?(?=\")', response.content)
            self.crawl(link_list[0], callback=self.detail_page_weixin)
        else:
            content = response.content
            tree = etree.HTML(content)
            title = tree.xpath("//div[@class='title']/text()")
            #text = tree.xpath("//div[@class='WB_editor_iframe']//p/text()")
            article_time = tree.xpath("//span[@class='time']/text()")
            images = tree.xpath("//img[@node-type='articleHeaderPic']/@src")
            image2 = tree.xpath("//div[@class='WB_editor_iframe']//img/@src")
            images.extend(image2)
            soup = BeautifulSoup(response.content)
            text=soup.select('div[class="WB_editor_iframe"]')
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
                "Content": format_content.format_content(content.replace("visibility: hidden","")),
                "AddTime": article_time[0][-23:-4].encode("utf8"),
                "Images": ",".join(images),
                "ImageNum":len(images),
                "Language": 1,
                "NewsSource": "微博",
                "Link":response.url,
                "PlainText":text,
            }
            sql.into(**data)
            return data


    @config(priority=2)
    def detail_page_weixin(self, response):
        sql = ToMysql()
        if "weixin" in response.url:
            content = response.content
            tree = etree.HTML(content)
            title = tree.xpath("//h2[@class='rich_media_title']/text()")
            article_time = tree.xpath("//em[@id='post-date']/text()")
            images = tree.xpath("//img/@data-src")
            soup = BeautifulSoup(content)
            text=soup.select('div[id="js_content"]')
            images2=[]
            content = str(text[0])
            sql = ToMysql()
            format_content = FormatContent()
            data = {
                "Title": "".join(title).replace("\r","").replace("\n","").replace(" ",""),
                "Content": format_content.format_content(content),
                "AddTime": "".join(article_time),
                "Images": ",".join(images),
                "ImageNum":len(images),
                "Language": 1,
                "NewsSource": "微博",
                "Link":response.url
            }
            #sql.into(**data)
            #return data
        if "weibo" in response.url:
            content = response.content
            tree = etree.HTML(content)
            title = tree.xpath("//div[@class='title']/text()")
            text = tree.xpath("//div[@class='WB_editor_iframe']//p/text()")
            article_time = tree.xpath("//span[@class='time']/text()")
            images = tree.xpath("//img[@node-type='articleHeaderPic']/@src")
            image2 = tree.xpath("//div[@class='WB_editor_iframe']//img/@src")
            images.extend(image2)
            data = {
                "title": "".join(title),
                "text": "".join(text).replace("\n",""),
                "article_time": "".join(article_time),
                "spider_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                "image_1": images[0] if len(images) >= 1 else None,
                "image_2": images[1] if len(images) >= 2 else None,
                "image_3": images[2] if len(images) >= 3 else None,
                "source": "weibo",
                "tab":0,
            }
            #sql.into(**data)
            #return data
