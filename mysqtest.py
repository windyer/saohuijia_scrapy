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
#aa =cur.execute("select AddTime from tb_news")
bb = cur.execute("select * from tb_news  where NewsSource = 'nzherald' ")

print bb
info = cur.fetchmany(bb)
print info[-4][-5]

cur.close()
conn.commit()
conn.close()
