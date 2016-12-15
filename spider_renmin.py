#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-15 22:52:36
# Project: renmin

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.page_count = 2
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
        for page in range(self.page_count):
            self.data['curpage'] = page
            url = "http://search.people.com.cn/rmw/GB/rmwsearch/gj_searchht.jsp"
            self.crawl(url, callback=self.index_page,method='POST', data=self.data)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
