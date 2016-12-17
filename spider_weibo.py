#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-17 11:50:37
# Project: weobo

from pyspider.libs.base_handler import *
from lxml import etree
from newspaper import Article
import re

class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.page_count = 5
        self.urls = "http://weibo.cn/purenewzealand?page={0}&vt=4"

        self.cookie = {
            "SUB": "_2A251UNq6DeRxGeRI7lsT8ybJyDmIHXVWuubyrDV6PUJbkdANLRPAkW1Fe9TmFJzJbLhmC2N0qb7Q8J4G-w..",
            "_T_WM": "48682eca346fd5756be3d656e13d9cf7",
            "gsid_CTandWM": "4uu276891Ue2EncKXE3ynb9MW8D",
        }

    @every(minutes=60)
    def on_start(self):
        for page in range(self.page_count):
            url = self.urls.format(str(page))
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
            time = tree.xpath("//span[@class='time']/text()")
            image = tree.xpath("//img[@node-type='articleHeaderPic']/@src")
            image2 = tree.xpath("//div[@class='WB_editor_iframe']//img/@src")
            image.extend(image2)
            return {
                "title": title[0].encode("utf8"),
                "text": "".join(text),
                "time": time[0],
                "image": image
            }

    @config(priority=2)
    def detail_page_weixin(self, response):
        if "weixin" in response.url:
            content = response.content
            tree = etree.HTML(content)
            text = tree.xpath("//span/text()")
            title = tree.xpath("//h2[@class='rich_media_title']/text()")
            time = tree.xpath("//em[@id='post-date']/text()")
            image = tree.xpath("//img/@data-src")
            return {
                "title": "".join(title),
                "text": "".join(text),
                "time": time[0],
                "image": image[1:-1]
            }
        else:
            content = response.content
            tree = etree.HTML(content)
            title = tree.xpath("//div[@class='title']/text()")
            text = tree.xpath("//div[@class='WB_editor_iframe']//p/text()")
            time = tree.xpath("//span[@class='time']/text()")
            image = tree.xpath("//img[@node-type='articleHeaderPic']/@src")
            image2 = tree.xpath("//div[@class='WB_editor_iframe']//img/@src")
            image.extend(image2)
            return {
                "title": title[0].encode("utf8"),
                "text": "".join(text),
                "time": time[0],
                "image": image
            }