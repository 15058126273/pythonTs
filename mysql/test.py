#  encoding=utf-8

import pymysql


conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='1234',
    db='python',
    charset='utf8'
    )

cur = conn.cursor()

cur.execute('create table images (\
            id int(10) , \
            img_path varchar(255), \
            add_date timestamp, \
            name varchar(255), \
            primary key(id) \
            )')


# cur.execute("select * from n_user_info limit 0,20")
# for data in cur:
#     print(str(data))
