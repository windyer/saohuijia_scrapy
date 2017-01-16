import requests
from lxml import etree
import re
import json
data={
    "type":"WHOLE_SITE",
    "keyword":"%E6%96%B0%E8%A5%BF%E5%85%B0",
    "x":"18",
    "y":"12",
}
Cookie={
'TRACKID':'bf1b463dcf2de2ae32e08e3d3d1a9422', 'etnetsessionid':'1d46244cfdd543cca5df1cf6f3b8df4b', 'Hm_lvt_d48efa75a1d1f8886429953ef54a13ec':'1484125462','Hm_lpvt_d48efa75a1d1f8886429953ef54a13ec':'1484125894'
}
rep=requests.post("http://www.etnet.com.cn/etnetChina/searchSite",data,cookies=Cookie)
content= rep.content
print content

#article = Article("http://world.people.com.cn/n1/2016/1207/c1002-28930757.html", language='zh')
#article.download()
#article.parse()
#print article.title,article.text,article.top_image