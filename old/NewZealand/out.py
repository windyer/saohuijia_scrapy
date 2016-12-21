import os

import requests

from connet import Connect


class out:

    def __init__(self,Text):
        self.con = Connect.Connect()
        self.db = self.con.dbConnect()
        self.cursor = self.db.cursor()
        self.Text = Text


    def news_info(self, Url, Content, Src, Lanuage, NewSource):
        Content = Content.replace("<a","<strong")
        Content = Content.replace("</a>","</strong>")
        Content = Content.replace("\n","")
        Content = Content.replace('"',"\\'")
        Q = "<html><head><style type='text/css'>div{" \
            "width : 100%;" \
            "}" \
            "p{" \
            "    text-indent: 2em;" \
            "    font-family: 'Merriweather Sans',Open Sans,Helvetica,Arial,sans-serif;" \
            "    font-size: 1rem;" \
            "    font-weight: lighter;" \
            "    line-height: 120%;" \
            "    margin: 0 0 10px;" \
            "    padding: 15px 15px 15px 15px;" \
            "    color: black;"\
            "}" \
            "img" \
            "{" \
            " display:block; " \
            " margin:0 auto;" \
            "width: 100%;" \
            "display: block;" \
            "margin: auto;" \
            "}" \
            "a{" \
            " color: #2ba4eb;" \
            " text-decoration: none;" \
            "}" \
            "</style>" \
            "</head>" \
            "<body>" \
            "<div>"
        Q = Q.replace("'","\\'")
        H = "</div></body></html>"
        Content =  Q + Content + H
        Srcs = '_'.join(Src)
        sql = "insert into tb_news(Title,Content,AddTime,Language, Images, ImageNum, NewsSource, Link) " \
              "value ('%s','%s','%s','%d', '%s', '%d','%s', '%s')"% \
              (self.Text[0], Content, self.Text[1], int(Lanuage), Srcs, len(Src), NewSource, Url)
        select = "select Id from tb_news where Title = '%s'"%self.Text[0]
        #判断是否存在
        try:
            self.cursor.execute(select)
            if self.cursor.fetchone():
                pass
            else:
                self.cursor.execute(sql)
                self.db.commit()
                # 保存图片到本地
                # id = self.cursor.lastrowid
                # self.img(Src, id)
        except Exception as e:
            print("写入%s失败"%self.Text[0])



    #保存图片
    def img(self, Srcs, id):
        i = 0
        for Tmp in Srcs:
            try:
                root = "Img/"+str(id)
                isExists = os.path.exists(root)
                if not isExists:
                    os.mkdir("Img/" + str(id))
                r = requests.get(Tmp, stream=True)
                string = 'Img/' + str(id) + '/' + str(i) + '.jpg'
                fp = open(string, 'wb')
                fp.write(r.content)
                fp.close()
                i += 1
            except Exception as e:
                print(Tmp)