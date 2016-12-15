from newspaper import Article
article = Article("http://www.fmprc.gov.cn/web/gjhdq_676201/gj_676203/dyz_681240/1206_681940/1206x2_681960/t1412689.shtml",language='zh')
article.download()
article.parse()
print article.text
print article.title
print article.images