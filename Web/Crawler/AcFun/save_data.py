# -*- encoding=utf-8 -*-
"""
    python: 3.5
    author: yjy
    date: 2016-9-22
    desc: 保存数据到mysql 数据库
"""
import pymysql


def save(video, update):
    """
    保存 or 更新数据
    :param video: 数据包
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
        video_id = video.get('id')
        link = video.get('link')
        video_name = video.get('video_name')
        collect_num = video.get('collect_num')
        view_num = video.get('view_num')
        comment_num = video.get('comment_num')
        dan_num = video.get('dan_num')
        banana_num = video.get('banana_num')
        if update:
            sql = 'update ac_video set CHANGE where id = '+str(video_id)
            change = ''
            value = []
            if link is not None:
                change += 'link=%s,'
                value.append(link)
            if video_name is not None:
                change += 'video_name=%s,'
                value.append(video_name)
            if collect_num is not None:
                change += 'collect_num=%s,'
                value.append(collect_num)
            if view_num is not None:
                change += 'view_num=%s,'
                value.append(view_num)
            if comment_num is not None:
                change += 'comment_num=%s,'
                value.append(comment_num)
            if dan_num is not None:
                change += 'dan_num=%s,'
                value.append(dan_num)
            if banana_num is not None:
                change += 'banana_num=%s,'
                value.append(banana_num)
            if change.endswith(','):
                change = change[:-1]
            sql = sql.replace('CHANGE', change)
            cur.execute(sql, tuple(value))
        else:
            sql = 'insert into ac_video (COLUMN) values (VALUES)'
            column = ''
            values = ''
            value = []
            if video_id is not None:
                column += 'id'
                value.append(video_id)
                values += '%s'
            if link is not None:
                column += ',link'
                value.append(str(link))
                values += ',%s'
            if video_name is not None:
                column += ',video_name'
                value.append(str(video_name))
                values += ',%s'
            if collect_num is not None:
                column += ',collect_num'
                values += ',%s'
                value.append(str(collect_num))
            if view_num is not None:
                column += ',view_num'
                values += ',%s'
                value.append(str(view_num))
            if comment_num is not None:
                column += ',comment_num'
                values += ',%s'
                value.append(str(comment_num))
            if dan_num is not None:
                column += ',dan_num'
                values += ',%s'
                value.append(str(dan_num))
            if banana_num is not None:
                column += ',banana_num'
                values += ',%s'
                value.append(str(banana_num))
            sql = sql.replace('COLUMN', column).replace('VALUES', values)
            cur.execute(sql, tuple(value))
        conn.commit()
    except:
        pass
    finally:
        cur.close()
        conn.close()


