from bs4 import BeautifulSoup
import random
import time

class Spider_sky:

    def __init__(self, text):
        self.text = text
        self.Soup = BeautifulSoup(text, 'html.parser')



    def get_list(self):
        Ttile = self.Soup.find_all(class_="it-article-headline other_headline")
        Src = []
        for Tmp in Ttile:
            Src.append(Tmp.find("a")['href'])
        return Src

    def get_info(self):
        title = self.Soup.find('div', class_="story_content_top mbm cf").find('h1').get_text()
        title = title.replace("'","")
        title = title.replace("\n","")
        title = title.rstrip()
        author = self.Soup.find('span', itemprop="name").get_text()
        Time = self.Soup.find('span', itemprop="datePublished")['content']
        t = time.strptime(Time, "%a %b %d %X UTC %Y")
        Time = time.strftime("%Y-%m-%d %X",t)
        Info = self.Soup.find('article', class_='story_landing').find_all('p', class_="")
        Img = self.Soup.find('article', class_='story_landing').find_all('div', class_="landscapephoto")
        for Tmp in Img:
            Info.insert(random.randint(0, len(Info)), Tmp.find('img'))
        Data = ''
        for Tmp in Info:
            Data = Data + str(Tmp)
        return title,Time,author,Data

    def get_src(self):
        img = self.Soup.find_all('div', class_='landscapephoto')
        Srcs = []
        for item in img:
            Srcs.append(item.find('img')['src'])
        return Srcs