#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-28 11:30:29
# Project: nzherald

import json
from newspaper import Article
from pyspider.libs.base_handler import *
from lxml import etree
from mysql_conf import ToMysql
import datetime
from bs4 import BeautifulSoup
from mysql_conf import FormatContent
from qiniu_update import update

class Handler(BaseHandler):
    crawl_config = {
    }
    def __init__(self):
        self.page = 2
        self.url = "http://www.nzherald.co.nz/json/sitesearch/index.cfm?&KW1=china&layout=all&order=Date&pageno={0}&timespan=all&init=china"
        self.url2 = "http://www.nzherald.co.nz/json/sitesearch/index.cfm?&KW1=china&layout=all&order=Date&pageno={0}&timespan=all&init=chinese"
        self.moon = {
            'Jan': 'January',
            'Feb ': 'February',
            'Mar': 'March',
            'Apr': 'April',
            'May': 'May',
            'June': 'June',
            'July': 'July',
            'Aug': 'Aguest',
            'Sept': 'September',
            'Oct': 'October',
            'Nov': 'November',
            'Dec': 'December'
            }

    @every(minutes=24 * 60)
    def on_start(self):
        urls=[]
        for i in range(self.page):
            urls.append(self.url.format(str(i+1)))
            urls.append(self.url2.format(str(i + 1)))
        self.crawl(urls, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        content = response.content
        js_data = json.loads(unicode(content, errors='ignore'))
        for url in js_data['DATA']['RESULTS']:
            self.crawl("http://www.nzherald.co.nz" + url['linkurl'], callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        title = tree.xpath("//h1[@id='articleTitle']/text()")
        article_time = tree.xpath("//span[@class='floatLeft storyDate']/text()")
        soup = BeautifulSoup(response.content)
        text = soup.select('div[class="articleBody"]')
        content = str(text[0])
        images = tree.xpath("//div[@class='articleBody']//img/@src")
        images2=[]
        for image in images:
            if image !='':
                new_image=update.load(image, "nzherald")
                images2.append(new_image)
                content=content.replace(image,new_image)
        soup2 = BeautifulSoup(content)
        s=[s.extract() for s in soup2('section')]
        tree = etree.HTML(str(soup2))
        #imgs = soup2.select('img')
        #for img, img2 in zip(imgs, images2):
        #    content = content.replace(img['src'], img2.encode("utf8"))
        sql = ToMysql()
        format_content = FormatContent()
        t = "".join(article_time)
        for i in self.moon.keys():
            if i in t:
                t = t.replace(i,self.moon[i])
        data = {
            "Title": "".join(title),
            "Content": format_content.format_content(str(soup2)),
            "AddTime": str(datetime.datetime.strptime(t[8:],'%A %B %d, %Y'))[:10],
            "Images": ",".join(images2),
            "ImageNum": len(images2),
            "Language": 0,
            "NewsSource": "nzherald",
            "Link": response.url
        }
        #try:
        #    sql.into(**data)
        #except:
        #    raise
        return data
