# -*- encoding=utf-8 -*-
"""
    python: 3.5
    author: yjy
    date: 2017-2-3
    desc: 保存数据到mysql 数据库
"""
import pymysql


def save(content):
    """
    保存 or 更新数据
    :param content: 数据包
    :param update: 是否是更新 true代表更新否则保存
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
        id = content.get('id')
        link = content.get('link')
        name = content.get('name')
        fun = content.get('fun')
        comment = content.get('comment')
        sql = 'insert into qsbk (COLUMN) values (VALUES)'
        column = ''
        values = ''
        value = []
        if id is not None:
            column += 'id'
            value.append(id)
            values += '%s'
        if link is not None:
            column += ',link'
            value.append(str(link))
            values += ',%s'
        if name is not None:
            column += ',name'
            value.append(str(name))
            values += ',%s'
        if fun is not None:
            column += ',fun'
            values += ',%s'
            value.append(fun)
        if comment is not None:
            column += ',comment'
            values += ',%s'
            value.append(comment)
        sql = sql.replace('COLUMN', column).replace('VALUES', values)
        cur.execute(sql, tuple(value))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()


def checkdatabase():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='yjy',
        passwd='yyyyyy',
        db='yjy',
        charset='utf8'
    )
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS qsbk ( \
                id INT(11), \
                name VARCHAR(100), \
                link VARCHAR(255), \
                fun INT(11), \
                comment INT(11),  primary key (id)) ; ')

