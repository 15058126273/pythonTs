import http.client as http
import urllib
import time
import random
import math


# 测试的服务器 + 端口 （有些大网站会认定你是攻击并且重置你的请求，比如baidu.com）
SERVER_NAME = "www.langsspt.com"
# 访问的页面
URL = '/index.php/Index/verify'

SEND_NUM = 0


def test_start():
    test_data = {'phone': 15858654523}
    test_data_encode = urllib.parse.urlencode(test_data)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    conn = http.HTTPConnection(SERVER_NAME)
    # conn.request("POST", URL, test_data_encode, headers)
    conn.request("GET", URL+'?'+str(time.time()))
    res = conn.getresponse()
    if res.status == 200:
        res_body = res.read()
        res = open('result.txt', 'wb')
        res.write(res_body)
        res.close()
    else:
        print('status:', res.status)
    conn.close()

test_start()
