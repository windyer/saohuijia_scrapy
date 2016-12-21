from bs4 import BeautifulSoup

class url_info:

    def __init__(self, text):
        self.Soup = BeautifulSoup(text, 'html.parser')


    def get_info(self):
        Title = self.Soup.find("h1", class_="article-title")
        Time = self.Soup.find("span", class_="time")
        Content = self.Soup.find("div", class_="article-content").find_all('p', class_='')
        data = ''
        for Tmp in Content:
            data = data + str(Tmp)
        return Title.get_text(),Time.get_text(),data

    def get_src(self):
        Content = self.Soup.find("div", class_="article-content").find_all("img")
        Src = []
        for tmp in Content:
            Src.append(tmp['src'])
        return Src
