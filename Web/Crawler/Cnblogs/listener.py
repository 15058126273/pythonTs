# -*- encoding=utf-8 -*-
"""
    python: 3.5
    author: yjy
    time: 2016-10-3
    desc: 用于监控爬虫的进程,数据等
"""

import main

def check_links():
    print(len(main.all_links))


check_links()