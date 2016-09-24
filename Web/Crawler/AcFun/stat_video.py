# -*- encoding=utf-8 -*-
"""
    python: 3.5
    author: yjy
    time: 2016-09-24
    desc: 统计acfun所有视频
"""
import pymysql


class StatAF:
    def __init__(self):
        pass

    def get_conn(self):
        """
        获取数据库连接
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
        return conn

    def get_top(self, mold, top):
        """
        按mold统计最好的前top个视频
        :param mold: 类别 view_num:观看量 collect_num:收藏量 dan_num:弹幕数 comment_num:评论数 banana:香蕉数
        :param top: 统计前多少个,比如前一百个:top=100
        :return:
        """
        data = ()
        conn = self.get_conn()
        cur = conn.cursor()
        try:
            sql = 'select id,link,video_name from ac_video order by '+mold+' desc limit 0,'+str(top)
            cur.execute(sql)
            data = cur.fetchall()
        except:
            pass
        finally:
            conn.commit()
            cur.close()
            conn.close()
            return data

    def make_li(self, mold, top):
        data = self.get_top(mold, top)
        if data:
            li_file = open('li.txt', 'w')
            i = 1
            for v in data:
                name = v[2].replace(' - AcFun弹幕视频网 - 认真你就输啦 (・ω・)ノ- ( ゜- ゜)つロ', '')
                li = '<a href="'+v[1]+'" target="_blank"><li class="listLi"'
                li += ' title="'+name+'"\>'+str(i)+'.'+name+'</li></a>\n'
                li_file.seek(0, 2)
                li_file.write(li)
                i += 1
            li_file.close()


sa = StatAF()
sa.make_li('banana_num', 100)
