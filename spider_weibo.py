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

class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.page_count = 10
        self.urls = "http://weibo.cn/purenewzealand?page={0}&vt=4"

        self.cookie = {
            "SUB": "_2A251UNq6DeRxGeRI7lsT8ybJyDmIHXVWuubyrDV6PUJbkdANLRPAkW1Fe9TmFJzJbLhmC2N0qb7Q8J4G-w..",
            "_T_WM": "48682eca346fd5756be3d656e13d9cf7",
            "gsid_CTandWM": "4uu276891Ue2EncKXE3ynb9MW8D",
        }

    @every(minutes=60)
    def on_start(self):
        for page in range(self.page_count):
            url = self.urls.format(str(page+1))
            self.crawl(url, callback=self.index_page, cookies=self.cookie)

    @config(age=60 * 60)
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
            text = tree.xpath("//div[@class='WB_editor_iframe']//p/text()")
            article_time = tree.xpath("//span[@class='time']/text()")
            images = tree.xpath("//img[@node-type='articleHeaderPic']/@src")
            image2 = tree.xpath("//div[@class='WB_editor_iframe']//img/@src")
            images.extend(image2)
            sql = ToMysql()
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
            sql.into(**data)
            return data


    @config(priority=2)
    def detail_page_weixin(self, response):
        sql = ToMysql()
        if "weixin" in response.url:
            content = response.content
            tree = etree.HTML(content)
            text = tree.xpath("//span/text()")
            title = tree.xpath("//h2[@class='rich_media_title']/text()")
            article_time = tree.xpath("//em[@id='post-date']/text()")
            images = tree.xpath("//img/@data-src")
            data = {
                "title": "".join(title),
                "text": "".join(text).replace("\n",""),
                "article_time": "".join(article_time),
                "spider_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                "image_1": images[1] if len(images) >= 2 else None,
                "image_2": images[2] if len(images) >= 3 else None,
                "image_3": images[3] if len(images) >= 3 else None,
                "source": "weibo",
                "tab":0,
            }
            sql.into(**data)
            return data
        else:
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
            sql.into(**data)
            return data
