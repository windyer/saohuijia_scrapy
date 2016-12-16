#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-16 15:46:45
# Project: chinesenzherald

from pyspider.libs.base_handler import *
from lxml import etree

class Handler(BaseHandler):
    crawl_config = {
    }
    def __init__(self):
        self.article_cout =10
        self.urls={
            "http://www.chinesenzherald.co.nz/news/new-zealand/?start=":u"新西兰",
            "http://www.chinesenzherald.co.nz/news/international/?start=":u"国际",
            "http://www.chinesenzherald.co.nz/news/lifestyle/?start=":u"生活",
            "http://www.chinesenzherald.co.nz/news/property/?start=":u"房产",
            "http://www.chinesenzherald.co.nz/news/travel/?start=":u"旅游",
            "http://www.chinesenzherald.co.nz/news/entertainment/?start=":u"娱乐",
            "http://www.chinesenzherald.co.nz/news/socialmedia/?start=":u"自媒体",
              }
    @every(minutes=24 * 60)
    def on_start(self):
        url_list=[]
        for url in self.urls:
            for i in range(self.article_cout)[::10]:
                     url_list.append(url+str(i))
        self.crawl(url_list, callback=self.index_page)

    @config(age=24 * 60 * 60)
    def index_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        urls = tree.xpath("//h4//a/@href")
        urls2 = tree.xpath("//div[@class='sidebar']//a/@href")
        urls.extend(urls2)
        for url in urls:
            self.crawl("http://www.chinesenzherald.co.nz" +url, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        image = tree.xpath("//div[@class='social-links-article-container']//img/@src")
        t = 0
        for i in image:
            image[t] = "http://www.chinesenzherald.co.nz/" + i
            t += 1
        text = tree.xpath("//div[@class='article-page__content']//p/text()")
        title = tree.xpath("//h1/text()")
        time = tree.xpath("//span[@class='article-page__header__date']/text()")
        return {
            "title": title[0].encode("utf8"),
            "text":"".join(text),
            "time":time[0],
            "image":image,
        }
