#  encoding=utf-8

import http.client as http
import urllib
import time
import random
import math


# 测试的服务器 + 端口 （有些大网站会认定你是攻击并且重置你的请求，比如baidu.com）
SERVER_NAME = "www.langsspt.com"
# SERVER_NAME = "www.zx195.com"
# 访问的页面
URL = '/index.php/Index/msgSend'
# URL = '/index.php/Index/verify'


def test_start():
    test_data = {'phone': 13968042920, 'imgcode': 1456}
    test_data_encode = urllib.parse.urlencode(test_data)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36\
                        (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'ktime_20160611/www.langsspt.com=-2;\
                    PHPSESSID=ct4r7jt2fs9u74f1tbtlg8hcd6;\
                    CNZZDATA1259850767=1547586482-1470885066-%7C1473654407',
        'X-Requested-With': 'XMLHttpRequest'

    }
    conn = http.HTTPConnection(SERVER_NAME)
    conn.request("POST", URL, test_data_encode, headers)
    # conn.request("GET", URL)
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
