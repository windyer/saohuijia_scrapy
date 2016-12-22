import pymysql.cursors

class Connect:
    def __init__(self):
        self.host = '52.78.198.99'
        self.user = 'nzbdt'
        self.password = '123456'
        self.db = 'nzbdtdb'
        self.charset = 'utf8mb4'
        self.cursorClass = pymysql.cursors.DictCursor

    def dbConnect(self):
        try:
            connection = pymysql.connect(host=self.host,
                                         user=self.user,
                                         password=self.password,
                                         db=self.db,
                                         charset=self.charset,
                                         cursorclass=self.cursorClass)
            return connection
        except:
            print('连接失败')
