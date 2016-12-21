#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-15 22:52:36
# Project: renmin

from pyspider.libs.base_handler import *
import re
from newspaper import Article
from lxml import etree
from mysql_conf import ToMysql
import time

class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.page_count = 50
        self.data = {
            "basenames": "rmwsite",
            "where": "(CONTENT=(新西兰) or TITLE=(新西兰) or AUTHOR=(新西兰)) and (CLASS2=国际)",
            "curpage": 1,
            "pagecount": 20,
            "classvalue": "ALL",
            "classfield": "CLASS3",
            "isclass": 1,
            "keyword": "新西兰",
            "sortfield": "LIFO",
            "id": 0.8854089527904285,
            "_": "",
        }

    @every(minutes=24 * 60)
    def on_start(self):
        self.data['pagecount'] = self.page_count
        url = "http://search.people.com.cn/rmw/GB/rmwsearch/gj_searchht.jsp"
        self.crawl(url, callback=self.index_page,method='POST', data=self.data)

    @config(age=60 * 60)
    def index_page(self, response):
        link_list = re.findall(r"http.+?html",response.content)
        for url in link_list:
            if "2012" not in url:
                self.crawl(url, callback=self.detail_page, validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        tree = etree.HTML(response.content)
        article_time = tree.xpath("//div[@class='fl']/text()")
        txt = tree.xpath("//div[@class='box_con']//p/text()")
        title = tree.xpath("//h1//text()")
        images = tree.xpath("//div[@class='box_con']//img/@src")
        images2=[]
        for image in images:
            if "http" in image:
                images2.append(image)
        sql = ToMysql()
        data = {
            "title": "".join(title),
            "text": "".join(txt),
            "article_time": article_time[0][-23:-5].encode("utf8"),
            "spider_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "image_1": images[0] if len(images) >= 1 else None,
            "image_2": images[1] if len(images) >= 2 else None,
            "image_3": images[2] if len(images) >= 3 else None,
            "source": "renmin",
            "tab": 0,
        }
        sql.into(**data)
        return data

