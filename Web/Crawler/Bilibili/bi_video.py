# -*- encoding=utf-8 -*-
"""
    python: 3.5
    author: yjy
    date: 2016-9-23
    desc: 抓取bilibili网站的所有视频信息
"""
import urllib.parse
import urllib.request
import save_data
import re
import threading
import gzip
import io


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
                url = 'http://www.bilibili.com/video/av'+str(id)+'/?tg'
                response = self.opener.open(url)
                if response.info().get('Content-Encoding') == 'gzip':
                    buf = io.BytesIO(response.read())
                    f = gzip.GzipFile(fileobj=buf)
                    data = f.read()
                else:
                    data = response.read()
                data = data.decode()
                if data is not None and '<title>' in data:
                    data_str = urllib.parse.unquote(str(data))
                    res = re.search(r'<title>(.*)</title>', data_str)
                    title = res.group(1)
                    if res is not None and title:
                        if title != '哔哩哔哩弹幕视频网 - ( ゜- ゜)つロ  乾杯~  - bilibili' and '_bilibili_哔哩哔哩弹幕视频网' in title:
                            title = title.replace('_bilibili_哔哩哔哩弹幕视频网', '')
                            video = {'id': id, 'video_name': title, 'link': url}
                            save_data.save(video, False)
                            self.get_data(id)
            except:
                pass
        else:
            end_threads += 1
            result()

    def get_data(self, id):
        try:
            url = 'http://api.bilibili.com/archive_stat/stat?aid='+str(id)
            response = self.opener.open(url)
            data = response.read().decode()
            if data is not None:
                data_dict = eval(data)
                if data_dict.get('message') == 'ok':
                    data_video = data_dict.get('data')
                    video = {'id': id,
                             'collect_num': data_video['favorite'],
                             'view_num': data_video['view'],
                             'dan_num': data_video['danmaku'],
                             'coin_num': data_video['coin'],
                             'share_num': data_video['share'],
                             'comment_num': data_video['reply']
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
start(4500000, 6000000, 100)


