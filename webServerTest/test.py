import http.client as http
import urllib
import random
import math


# 测试的服务器 + 端口 （有些大网站会认定你是攻击并且重置你的请求，比如baidu.com）
SERVER_NAME = "www.yjytomcat.com:8080"
# 访问的页面
URL = '/'


def test_start():
    # 配置conn
    conn = http.HTTPConnection(SERVER_NAME)
    conn.request("GET", URL)
    res = conn.getresponse()
    if res.status == 200:
        res_body = res.read()
        res_file = open('result.txt', 'wb')
        res_file.write(res_body)
        res_file.close()
    else:
        print('status:', res.status)
    conn.close()

test_start()
