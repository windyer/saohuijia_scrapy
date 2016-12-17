import requests
import json,re
from newspaper import Article
from lxml import etree
##urls=[]
#url="http://a.jiemian.com/index.php?m=search&a=index&msg=%E6%96%B0%E8%A5%BF%E5%85%B0&type=news&page={}"
#for i in range(50):
#    urls.append(url.format(str(i+1)))
#print urls
url = "http://www.kannz.com/"
cookie = {
    "SUB":"_2A251UNq6DeRxGeRI7lsT8ybJyDmIHXVWuubyrDV6PUJbkdANLRPAkW1Fe9TmFJzJbLhmC2N0qb7Q8J4G-w..",
    "_T_WM":"48682eca346fd5756be3d656e13d9cf7",
    "gsid_CTandWM":"4uu276891Ue2EncKXE3ynb9MW8D",

}
response = requests.get(url)
content=response.content
tree=etree.HTML(content)
urls = tree.xpath("//article[@class='excerpt']//header//h2//a/@href")
#urls2 = tree.xpath("//div[@class='sidebar']//a/@href")
#urls.extend(urls2)
urls2=[]
for i in urls:
    print i
    urls2.append(i)

#article = Article(urls2[0],language='zh')
#article.download()
#article.parse()
#print article.text
#print article.top_image
#print article.title
#
response = requests.get(urls2[0])
tree = etree.HTML(response.content)
txt = tree.xpath("//p/text()")
title = tree.xpath("//h1[@class='article-title']//a/text()")
image = tree.xpath("//article[@class='article-content']//img/@src")
print "".join(title),image,"".join(txt)
###t=0
###for i in images:
###    images[t] = "http://www.chinesenzherald.co.nz/"+i
###    t+=1
##response = requests.get("http://weibo.cn/sinaurl?f=w&u=http%3A%2F%2Ft.cn%2FRIh2s5I&ep=ElbYXo8bg%2C1663311732%2CElbYXo8bg%2C1663311732&vt=4",cookies=cookie)
##print response
##content=response.content
##print content
##
##link_list = re.findall(r'(?<=URL\=).+?(?=\")',response.content)
##print link_list
##
###text = tree.xpath("//div[@class='WB_editor_iframe']//p/text()")
###time = tree.xpath("//span[@class='time']/text()")
###image = tree.xpath("//img[@node-type='articleHeaderPic']/@src")
##title = tree.xpath("//h2[@class='rich_media_title']/text()")
##text = tree.xpath("//div[@class='rich_media_content']//span/text()")
##time = tree.xpath("//em[@id='post-date']/text()")
##image = tree.xpath("//img/@data-src")
#####print time[0][-23:-4].encode("utf8"),"".join(text),title[0].encode("utf8"),image
####
####print title[0].encode("utf8"),"".join(text),images,time[0]
###content=article.html
###tree=etree.HTML(content)
###time = tree.xpath("//div[@id='News_Body_Time']/text()")
##print title[0].encode("utf8"),"1111"
##print "".join(text),time,len(image)
##for i in image:
##    print i
###print time[0]
#print "".join(title),article.top_image,"".join(txt)