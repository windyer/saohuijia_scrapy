#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-15 22:52:36
# Project: renmin

from pyspider.libs.base_handler import *
import re
from newspaper import Article
from lxml import etree

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

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        link_list = re.findall(r"http.+?html",response.content)
        for url in link_list:
            self.crawl(url, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        tree=etree.HTML(response.content)
        time = tree.xpath("//div[@class='fl']/text()")
        url = response.url
        article=Article(url,language='zh')
        article.download()
        article.parse()
        return {
            "title": article.title,
            "text": article.text,
            "image":article.top_image,
            "time":time[0][:-5].encode("utf8")
        }
