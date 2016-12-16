import requests
import json
from newspaper import Article
from lxml import etree
##urls=[]
#url="http://a.jiemian.com/index.php?m=search&a=index&msg=%E6%96%B0%E8%A5%BF%E5%85%B0&type=news&page={}"
#for i in range(50):
#    urls.append(url.format(str(i+1)))
#print urls
url = "http://www.weibo.com/purenewzealand?is_hot=1"
response = requests.get(url)
content=response.content
tree=etree.HTML(content)
urls = tree.xpath("//a/@href")
#urls2 = tree.xpath("//div[@class='sidebar']//a/@href")
#urls.extend(urls2)
urls2=[]
for i in urls:
    if "htm" in i:
        if "http" not in i:
            i = url+i[2:]
        urls2.append(i)
print urls2

#article = Article("http://www.chinaembassy.org.nz/chn/zxgx/t1421705.htm",language='zh')
#article.download()
#article.parse()
##images = tree.xpath("//div[@class='social-links-article-container']//img/@src")
##t=0
##for i in images:
##    images[t] = "http://www.chinesenzherald.co.nz/"+i
##    t+=1
##text = tree.xpath("//div[@class='article-page__content']//p/text()")
##title = tree.xpath("//h1/text()")
##time = tree.xpath("//span[@class='article-page__header__date']/text()")
###print time[0][-23:-4].encode("utf8"),"".join(text),title[0].encode("utf8"),image
##
##print title[0].encode("utf8"),"".join(text),images,time[0]
#content=article.html
#tree=etree.HTML(content)
#time = tree.xpath("//div[@id='News_Body_Time']/text()")
#print article.text,"1111"
#print article.title,article.top_image
#print time[0]