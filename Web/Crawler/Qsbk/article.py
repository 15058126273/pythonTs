# -*- encoding=utf-8 -*-
"""
    python: 3.5
    author: yjy
    date: 2016-9-22
    desc: 抓取糗事百科
"""
import urllib.parse
import urllib.request
import save_data
import re
import threading
import socket
import requests
import time


class Qsbk:
    def __init__(self, start_id, end_id):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
                        }
        self.start_id = start_id
        self.end_id = end_id

    def check_exist(self):
        global end_threads
        while self.start_id <= self.end_id:
            try:
                id = self.end_id
                self.end_id -= 1
                url = 'http://www.qiushibaike.com/article/'+str(id)
                res = requests.get(url)
                print('正在处理第', id, '个内容, status:'+str(res.status_code))
                if res.status_code == 200:
                    data = res.content.decode()
                    if data is not None and '<title>' in data and '<i class="number">' in data:
                        data_str = urllib.parse.unquote(str(data))
                        data_str = data_str.replace("\n", "").replace(" ", "")
                        idMatch = re.search(r'<linkrel=\"canonical\"href=\"http://www.qiushibaike.com/article/(.*)\"/><metaname\="robots\"content=\"noarchive\">', data_str)
                        if idMatch and idMatch.group(1) and idMatch.group(1) == str(id):
                            res = re.search(r'<title>(.*)</title>', data_str)
                            res1 = re.search(r'<spanclass=\"stats-vote\"><iclass=\"number\">(.*)</i>好笑</span>', data_str)
                            res2 = re.search(r'</span><iclass=\"number\">(.*)</i>评论</span>', data_str)
                            if res is not None and res.group(1) and res1.group(1) and res2.group(1):
                                content = {'id': id, 'name': res.group(1), 'link': url, 'fun': res1.group(1), 'comment': res2.group(1)}
                                save_data.save(content)
                else:
                    print("id:"+str(id) + ":"+str(res.status_code))
            except Exception as e:
                print(e)
            time.sleep(1)
        else:
            end_threads += 1
            result()


def result():
    if end_threads == create_threads:
        print('结束了')


def start(start_id, end_id, thread_num):
    global create_threads
    i = 0
    threads = []
    qb = Qsbk(start_id, end_id)
    try:
        while i < thread_num:
            thread = threading.Thread(target=qb.check_exist, args={})
            thread.start()
            threads.append(thread)
            i += 1
    except Exception as e:
        print('出错了', e)
    finally:
        create_threads = len(threads)

create_threads = 0
end_threads = 0
start(10000, 118494738, 1)


