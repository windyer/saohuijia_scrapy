import requests
import json
from newspaper import Article
from lxml import etree
##urls=[]
#url="http://a.jiemian.com/index.php?m=search&a=index&msg=%E6%96%B0%E8%A5%BF%E5%85%B0&type=news&page={}"
#for i in range(50):
#    urls.append(url.format(str(i+1)))
#print urls
url = "http://www.skykiwichina.com/"
resp = requests.get(url)
content=resp.content
tree=etree.HTML(content)
urls = tree.xpath("//div[@id='m_left']")
for i in urls:
    print i