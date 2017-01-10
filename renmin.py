import requests
from lxml import etree
import re
import json
rep=requests.get("http://www.nzherald.co.nz/json/sitesearch/index.cfm?&KW1=china&layout=all&order=Date&pageno=1&timespan=all&init=china")
content= rep.content

js_data = json.loads(unicode( content , errors='ignore'))
for url in js_data['DATA']['RESULTS']:
    print "http://www.nzherald.co.nz"+url['linkurl']
#article = Article("http://world.people.com.cn/n1/2016/1207/c1002-28930757.html", language='zh')
#article.download()
#article.parse()
#print article.title,article.text,article.top_image