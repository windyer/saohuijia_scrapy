from six import itervalues
import MySQLdb

class ToMysql():

    def __init__(self):
        '''''
        kwargs = {  'host':'localhost',
                    'user':'root',
                    'passwd':'root',
                    'db':'others',
                    'charset':'utf8'}
        '''
        hosts    = '52.78.198.99'
        username = 'nzbdt'
        password = 'saohuijia@123456'
        database = 'nzbdtdb'
        charsets = 'utf8'
        self.tables = 'tb_news'
        self.connection = False
        try:
            self.conn = MySQLdb.connect(host = hosts,port=3306,user = username,passwd = password,db = database,charset = charsets)
            self.cursor = self.conn.cursor()
            self.cursor.execute("set names "+charsets)
            self.connection = True
        except Exception,e:
            print "Cannot Connect To Mysql!/n",e

    def escape(self,string):
        return '%s' % string

    def into(self,**values):

        if self.connection:
            tablename = self.escape(self.tables)
            if values:
                _keys = ",".join(self.escape(k) for k in values)
                _values = ",".join(['%s',]*len(values))
                sql_query = "insert into %s (%s) values (%s)" % (tablename,_keys,_values)
            else:
                sql_query = "replace into %s default values" % tablename
            try:
                if values:
                    self.cursor.execute(sql_query,list(itervalues(values)))
                else:
                    self.cursor.execute(sql_query)
                self.conn.commit()
                return True
            except Exception,e:
                raise e
