#coding=utf-8
import requests
from lxml import etree
import re
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
#rep=requests.post("http://search.people.com.cn/rmw/GB/rmwsearch/gj_searchht.jsp",data=data)
#content= rep.content
#print rep.cookies
#print content
#tree=etree.HTML(content)
#link_list =re.findall(r"(?<=http:).+?(?=html)" ,"asdadasdadasdhttp:\\pasasd.htmlsss")
#link_list = re.findall(r"(http://([\w-]+\.)+[\w-]+(/[\w_./?%&=]*)?.html )","afadgfadghttp:\\jhakdghfd.htmladgf")
link_list =re.findall(r"http.+?html" ,"asdadasdadasdhttp:\\pasasd.htmlsssasdadasdadasdhttp:\\pasasd.htmlsss")
print link_list