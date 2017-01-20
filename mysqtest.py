import MySQLdb

conn = MySQLdb.connect(
    host='52.78.198.99',
    port=3306,
    user='nzbdt',
    passwd='saohuijia@123456',
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
#aa =cur.execute("select AddTime from tb_news")
bb = cur.execute("select * from tb_news WHERE AddTime >= '2017-01-19'")
#cc = cur.execute("delete from tb_news where AddTime >= '2017-01-20'")
print bb
info = cur.fetchmany(bb)
#print info[2][-8]

cur.close()
conn.commit()
conn.close()
