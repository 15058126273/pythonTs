# -*- encoding=utf-8 -*-

import pymysql


def get_conn():
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="yjy",
        passwd="yyyyyy",
        db="yjy",
        charset="utf8"
    )
    return conn


def save(data):
    """
    插入数据库
    :param data: (dict) link:链接  data:内容
    :return:
    """
    conn = get_conn()
    cur = conn.cursor()
    if data and data.get("data"):
        try:
            sql = "insert into cnblogs (c_link,c_data) values (%s, %s)"
            cur.execute(sql, (data.get("link"), data.get("data")))
        except Exception as e:
            print(str(e)[:50])
        finally:
            conn.commit()
            cur.close()
            conn.close()


def check_link(link):
    """
    检查url是否符合条件,并检查是否重复
    :param link:
    :return: True:符合条件  False:不符合条件
    """
    flag = False
    conn = get_conn()
    cur = conn.cursor()
    try:
        sql = 'select count(*) from cnblogs where c_link = %s'
        cur.execute(sql, (link,))
        res = cur.fetchone()
        if res[0] == 0:
            flag = True
    except Exception as e:
        print(str(e)[:50])
    finally:
        cur.close()
        conn.close()
        return flag


