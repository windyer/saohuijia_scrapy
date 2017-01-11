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
from bs4 import BeautifulSoup
from mysql_conf import FormatContent
from qiniu_update import update

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

    @every(minutes=24*60)
    def on_start(self):
        self.data['pagecount'] = self.page_count
        url = "http://search.people.com.cn/rmw/GB/rmwsearch/gj_searchht.jsp"
        self.crawl(url, callback=self.index_page,method='POST', data=self.data)

    @config(age=12*60*60)
    def index_page(self, response):
        link_list = re.findall(r"http.+?html",response.content)
        for url in link_list:
            if "2012" not in url and "people" in url:
                self.crawl(url, callback=self.detail_page, validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        tree = etree.HTML(response.content)
        article_time = tree.xpath("//div[@class='fl']/text()")
        title = tree.xpath("//h1//text()")
        images = tree.xpath("//div[@class='box_con']//img/@src")
        soup = BeautifulSoup(response.content)
        text=soup.select('div[class="box_con"]')
        images2=[]
        content = str(text[0])
        for image in images:
            if image !='' and "http" not in image:
                new_image = update.load("http://world.people.com.cn"+image, "people")
                images2.append(new_image)
                content=content.replace(image,new_image)
            else:
                new_image = update.load(image, "people")
                images2.append(new_image)
                content = content.replace(image, new_image)
        sql = ToMysql()
        format_content = FormatContent()
        data = {
            "Title": "".join(title),
            "Content": format_content.format_content(content),
            "AddTime": article_time[0][-23:-5].replace(u"年","-").replace(u"月","-").replace(u"日"," ").encode("utf8"),
            "Images": ",".join(images2),
            "ImageNum":len(images),
            "Language": 1,
            "NewsSource": "人民网",
            "Link":response.url
        }
        sql.into(**data)
        return data

