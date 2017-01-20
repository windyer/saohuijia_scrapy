import requests
from lxml import etree
import re
import json
import urllib,urllib2
data={
    'contentKey':'%E6%96%B0%E8%A5%BF%E5%85%B0',
    'op' : 'single',
    'siteID' :'',
    'sort' : 'date'
}
Cookie={
'JSESSIONID':'BB40756D446BC6D107B98E407063D7D9'}
rep=requests.post("http://www.cqn.com.cn/search/servlet/SearchServlet.do",data,cookies=Cookie)
content= rep.content
print content

#article = Article("http://world.people.com.cn/n1/2016/1207/c1002-28930757.html", language='zh')
#article.download()
#article.parse()
#print article.title,article.text,article.top_image