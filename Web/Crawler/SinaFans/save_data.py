# -*- encoding=utf-8 -*-
"""
    python: 3.5
    author: yjy
    date: 2016-9-22
    desc: 保存数据到mysql 数据库
"""
import pymysql


def save(sina):
    """
    保存 or 更新数据
    :param sina: 数据包
    :return:
    """
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='yjy',
        passwd='yyyyyy',
        db='yjy',
        charset='utf8'
    )
    cur = conn.cursor()
    try:
        sina_id = sina.get('id')
        fans_num = sina.get('fans_num')
        nick_name = sina.get('nick_name')
        sql = 'insert into sina_fans (COLUMN) values (VALUES)'
        column = ''
        values = ''
        value = []
        if id is not None:
            column += 'id'
            value.append(sina_id)
            values += '%s'
        if fans_num is not None:
            column += ',fans_num'
            value.append(fans_num)
            values += ',%s'
        if nick_name is not None:
            column += ',nick_name'
            value.append(str(nick_name))
            values += ',%s'
        sql = sql.replace('COLUMN', column).replace('VALUES', values)
        cur.execute(sql, tuple(value))
        conn.commit()
    except:
        pass
    finally:
        cur.close()
        conn.close()

