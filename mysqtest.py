import MySQLdb

conn = MySQLdb.connect(
    host='139.224.0.100',
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
    db='nzbdtdb',
    charset="utf8"
)
cur = conn.cursor()
aa =cur.execute("desc tb_news")
#bb = cur.execute("decs tb_news")
print aa
info = cur.fetchmany(aa)
for i in info:
    print i

cur.close()
conn.commit()
conn.close()
