import MySQLdb

conn = MySQLdb.connect(
    host='52.78.198.99',
    port=3306,
    user='nzbdt',
    passwd='123456',
    db='nzbdtdb',
    charset="utf8"
)

conn1 = MySQLdb.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='holytreetech.com',
    db='card',
    charset="utf8"
)
cur = conn.cursor()
aa =cur.execute("select content from tb_news")
#bb = cur.execute(" show columns from tb_news")
print aa
#info = cur.fetchmany(aa)
#print info[-1][-1]

cur.close()
conn.commit()
conn.close()
