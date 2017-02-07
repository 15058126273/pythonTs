# -*- encoding=utf-8 -*-
"""
    python: 3.5
    author: yjy
    time: 2016-10-3
    desc: 对博客园进行一个全面爬取
"""

import urllib.request as request
import re
import save_data
import io
import gzip
import threading
import time

links = ['http://www.cnblogs.com/pick?time='+str(time.time())]
all_links = []


def controller():
    while True:
        if len(links):
            try:
                link = links.pop(0)
                link = check_link(link)
                if link and save_data.check_link(link):
                    open_url(link)
            except Exception as e:
                print('controller:', str(e)[:50])


def check_link(link):
    if link and 'cnblogs.com' in link and '.jpg' not in link and '.png' not in link \
            and '.gif' not in link and '.zip' not in link:
        if link.endswith('/'):
            link = link[0:len(link)-1]
        return link
    return None


def open_url(link):
    try:
        print("尝试打开", link)
        res = request.urlopen(link)
        if res.status == 200 and 'text/html' in res.info().get("Content-Type"):
            if res.info().get('Content-Encoding') == 'gzip':
                buf = io.BytesIO(res.read())
                f = gzip.GzipFile(fileobj=buf)
                data = f.read().decode()
            else:
                data = res.read().decode()
            title = re.search(r'<title>(.*)</title>', data).group(1)
            save_data.save({"link": link, "data": title})
            get_link(data)
    except Exception as e:
        print('open_url', str(e)[:50])


def get_link(data):
    res = re.findall('"(http://.*?)"', data)
    for s in res:
        if s not in all_links:
            all_links.append(s)
            links.append(s)


plan_threads = 100
now_threads = 0
threads = []
while now_threads < plan_threads:
    thread = threading.Thread(target=controller)
    thread.start()
    threads.append(thread)
    now_threads += 1
