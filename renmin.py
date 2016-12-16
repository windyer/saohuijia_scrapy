#coding=utf-8
import requests
from lxml import etree
import re
from newspaper import Article
data={

"basenames":"rmwsite",
"where":"(CONTENT=(新西兰) or TITLE=(新西兰) or AUTHOR=(新西兰)) and (CLASS2=国际)",
"curpage":2,
"pagecount":20,
"classvalue":"ALL",
"classfield":"CLASS3",
"isclass":1,
"keyword":"新西兰",
"sortfield":"LIFO",
"id":0.8854089527904285,
"_":"",
}
rep=requests.post("http://search.people.com.cn/rmw/GB/rmwsearch/gj_searchht.jsp",data=data)
content= rep.content
link_list =re.findall(r"http.+?html" ,content)
print link_list
detail = requests.get(link_list[1])
tree=etree.HTML(detail.content)
time = tree.xpath("//div[@class='fl']/text()")
print "222222",time[0][:-5].encode("utf8")
#article = Article("http://world.people.com.cn/n1/2016/1207/c1002-28930757.html", language='zh')
#article.download()
#article.parse()
#print article.title,article.text,article.top_image