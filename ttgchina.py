git #!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-01-20 14:40:31
# Project: ttgchina

from lxml import etree
from pyspider.libs.base_handler import *
from mysql_conf import ToMysql
import time
from bs4 import BeautifulSoup,Comment
from mysql_conf import FormatContent
from qiniu_update import update
import timer
import datetime


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.ttgchina.com/search.php?keyword=%E6%BE%B3%E6%96%B0', callback=self.index_page)

    @config(age=0)
    def index_page(self, response):
        content=response.content
        tree=etree.HTML(content)
        urls = tree.xpath("//table[@id='article']//a/@href")
        for i in urls:
            if "article_id" in i:
                self.crawl("http://www.ttgchina.com/"+i, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        content = response.content
        tree = etree.HTML(content)
        title = tree.xpath("//td[@class='title']/text()")
        article_time = tree.xpath("//div[@class='publish_info_dim']/text()")
        #images = tree.xpath("//table[@id='article_box']//img/@src")
        #soup = BeautifulSoup(content)
        text = tree.xpath('//table[@id="article_box"]//div/text()')
        #soup2 = BeautifulSoup(str(text[0]))
        #text = soup.select('td')
        #content = str(text[5])
        soup2 = BeautifulSoup("".join(text))
        s=[s.extract() for s in soup2('script')]
        image_tap =soup2.select('img')
        comments = soup2.findAll(text=lambda text:isinstance(text, Comment))
        [comment.extract() for comment in comments]
        content2 = str(soup2)
        content = str(soup2)
        images2 = []
        #for image,tap in zip(images,image_tap):
            #if image != '':
                #new_image = update.load(image, "ttgchina")
                #images2.append(new_image)
                #content = content.replace(image,new_image)
                #content2 = content2.replace(str(tap),"(url,"+str(image)+")")
        text = ''.join(BeautifulSoup(content2).findAll(text=True))
        sql = ToMysql()
        format_content = FormatContent()
        data = {
            "Title": "".join(title),
            "Content":format_content.format_content(str(content)),
            "AddTime":"".join(article_time).replace("\n","").replace("\t","").lstrip(),
            "Images": ",".join(images2),
            "ImageNum": len(images2),
            "Language": 0,
            "NewsSource": "ttgchina",
            "Link": response.url,
            "PlainText":text

        }
        #try:
        #    sql.into(**data)
        #except:
        #    raise
        return data
