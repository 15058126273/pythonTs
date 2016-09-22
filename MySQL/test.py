# encoding=utf-8
#
# Python 3.5
# 需要安装pymysql模块

import pymysql


conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='yjy',
    passwd='yyyyyy',
    db='yjy',
    charset='utf8'
    )

cur = conn.cursor()

cur.execute('insert into ac_video (id) VALUES (1)')

cur.execute("select * from ac_video")
for data in cur:
    print(str(data))

