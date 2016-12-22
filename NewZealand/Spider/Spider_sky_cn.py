from bs4 import BeautifulSoup

class Spider_sky_cn :

    def __init__(self, text):
        self.Parser = BeautifulSoup(text, "html.parser")



    def get_url(self):
        Info = self.Parser.find('div', id="main_left").find_all("ul")
        Data = []
        for Tmp in Info:
            Tmp = Tmp.find_all('li')
            for item in Tmp:
                Data.append(item.find('a')['href'])
        return Data


