#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-26 14:21:42
# Project: hamilton

from pyspider.libs.base_handler import *
from google import search

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        cookie = {
            "NID": "=87=W1O2fwB2TOy6QBABbe2CN4GloETgmQ0q0yd1r-Oz_7TRZ6FTdTk2WywgUCfLc0N3TI1FeChInHG0R1btIyIr_RJYqhJBvtRreyXREHg9rtuv9vmSYFFwtEVugZt4AW-8",
        }
        self.crawl("http://cse.google.com/cse?cof=FORID%3A9&cx=006730714154542492986%3Aoh6vl0ybuqy&ie=UTF-8&q=china&search+site=&siteurl=www.stuff.co.nz%2F&ref=&ad=n9&num=30&rurl=http%3A%2F%2Fwww.stuff.co.nz%2Fsearchresults%3Fcof%3DFORID%253A9%26cx%3D006730714154542492986%253Aoh6vl0ybuqy%26ie%3DUTF-8%26q%3Dchina%26Search%2BSite%3D%26siteurl%3Dwww.stuff.co.nz%252F%26ref%3D%26ss#gsc.tab=0&gsc.q=china&gsc.page=1", callback=self.index_page)

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
