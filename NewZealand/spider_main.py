import html_donwloader,url_manager
import demjson
from Spider import url_info
from Spider import Spider_sky
import out

class Spider:

    def __init__(self):
        self.news_url = url_manager.url_manager()     # 新闻内容Url管理器
        self.search_url = url_manager.url_manager()   # 新闻列表Url管理器
        self.html_downloader = html_donwloader.html_downloader()

    def craw(self):
        n=0
        while n <= 5:
            count = 20 * n
            root_url = 'http://www.toutiao.com/search_content/?offset=' + str(
                count) + '&format=json&keyword=%E6%96%B0%E8%A5%BF%E5%85%B0&autoload=true&count=20'
            self.search_url.add_new_url(root_url)
            n +=1
        while self.search_url.is_url():
            try:
                Url = self.search_url.get_url()   # 任意取出一条新闻列表Url
                Html = self.html_downloader.one_downloader(Url, 'get')
                TmpDate = demjson.decode(Html)
                # 添加新闻内容Url
                for Tmp in TmpDate['data']:
                    self.news_url.add_new_url(Tmp['display_url'])
                while self.news_url.is_url():
                    try:
                        Url_news = self.news_url.get_url()
                        Html = self.html_downloader.one_downloader(Url_news, 'get')
                        Parser = url_info.url_info(Html)
                        Src = Parser.get_src()
                        Tmp = Parser.get_info()
                        Content = str(Tmp[2])
                        Out = out.out(Tmp)
                        Out.news_info(Url_news, Content, Src, 1, '今日头条')
                    except Exception as e:
                        print(Url_news)
            except Exception as e:
                print(Url)


    def craw_en(self):
        type_url = url_manager.url_manager()
        info_url = url_manager.url_manager()
        list_url = url_manager.url_manager()
        type = ['national','world','business','technology','sport','entertainment','life-style','travel','motoring']
        type_url.add_new_urls(type)
        while type_url.is_url():
            root_Url = "http://www.stuff.co.nz/" + type_url.get_url()
            Tmp = self.html_downloader.one_downloader(root_Url, 'get')
            try:
                list_Parser = Spider_sky.Spider_sky(Tmp)
                Urls = list_Parser.get_list()
                list_url.add_new_urls(Urls)
                while list_url.is_url():
                    Html = self.html_downloader.one_downloader("http://www.stuff.co.nz" + list_url.get_url(), 'get')
                    html_parser = Spider_sky.Spider_sky(Html)
                    info = html_parser.get_info()
                    Content = str(info[3]).replace("'", ' ')
                    try:
                        html_out = out.out(info)
                        Src = html_parser.get_src()
                        if Content != '[]':
                            if Content.find('chinese') != -1 or Content.find('china') != -1:
                                html_out.news_info("http://www.stuff.co.nz" + list_url.get_url(), Content, Src, 0, 'stuff')
                    except Exception as e:
                        print("http://www.stuff.co.nz" + list_url.get_url())
            except Exception as e:
                print(root_Url)


    def craw_sky(self):
        root_url = "http://news.skykiwi.com/na/"

if __name__ == "__main__":
    obj_spider = Spider()
    obj_spider.craw()
    obj_spider.craw_en()