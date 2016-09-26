# -*- encoding=utf-8 -*-
"""
    python: 3.5
    author: yjy
    date: 2016-9-22
    desc: 抓取acfun网站的所有视频信息
"""
import urllib.parse
import urllib.request
import save_data
import re
import threading
import socket


class AcFun:
    def __init__(self, start_id, end_id):
        self.agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        self.proxy_handler = urllib.request.ProxyHandler(None)
        self.proxy_auth_handler = urllib.request.ProxyBasicAuthHandler
        self.opener = urllib.request.build_opener(self.proxy_handler, self.proxy_auth_handler)
        self.opener.addheaders = [
                ('User-Agent', self.agent)
            ]
        self.start_id = start_id
        self.end_id = end_id

    def check_exist(self):
        global end_threads
        while self.start_id <= self.end_id:
            try:
                id = self.start_id
                self.start_id += 1
                print('正在处理第', id, '个视频')
                url = 'http://www.acfun.tv/v/ac'+str(id)
                response = self.opener.open(url)
                data = response.read().decode()
                if data is not None and '<title>' in data:
                    data_str = urllib.parse.unquote(str(data))
                    res = re.search(r'<title>(.*)</title>', data_str)
                    if res is not None and res.group(1):
                        video = {'id': id, 'video_name': res.group(1), 'link': url}
                        save_data.save(video, False)
                        self.get_data(id)
            except:
                pass

        else:
            end_threads += 1
            result()

    def get_data(self, id):
        try:
            url = 'http://www.acfun.tv/content_view.aspx?contentId='+str(id)
            response = self.opener.open(url)
            data = response.read().decode()
            if data is not None:
                data_list = eval(data)
                video = {'id': id,
                         'collect_num': data_list[5],
                         'view_num': data_list[0],
                         'dan_num': data_list[2],
                         'banana_num': data_list[6],
                         'comment_num': data_list[1]
                         }
                save_data.save(video, True)
        except:
            pass


def result():
    if end_threads == create_threads:
        print('结束了')


def start(start_id, end_id, thread_num):
    global create_threads
    i = 0
    threads = []
    af = AcFun(start_id, end_id)
    try:
        while i < thread_num:
            thread = threading.Thread(target=af.check_exist, args={})
            thread.start()
            threads.append(thread)
            i += 1
    except Exception as e:
        print('出错了', e)
    finally:
        create_threads = len(threads)

create_threads = 0
end_threads = 0
start(924000, 999999, 10)


