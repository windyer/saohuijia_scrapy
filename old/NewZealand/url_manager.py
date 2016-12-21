

class url_manager:

    def __init__(self):
        self.url_new = set()
        self.url_old = set()


    # 添加单个url
    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.url_new and url not in self.url_old:
            self.url_new.add(url)


    # 批量添加url
    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    # 判断是否还有url
    def is_url(self):
        return len(self.url_new) != 0

    # 返回url数量
    def url_num(self):
        return len(self.url_new)

    # 任意返回url
    def get_url(self):
        One_url = self.url_new.pop()
        self.url_old.add(One_url)
        return One_url

