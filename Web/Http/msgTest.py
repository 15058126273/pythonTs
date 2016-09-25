#  encoding=utf-8

import http.client as http
import urllib


# 测试的服务器 + 端口 （有些大网站会认定你是攻击并且重置你的请求，比如baidu.com）
SERVER_NAME = "www.langsspt.com"
# 访问的页面
URL = '/index.php/Index/to_change'

headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) \
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
        'Cookie': '__cfduid=d1ae98ecef2f1d6aa9651fd439f59b6dc1473424968; \
                    ktime_20160611/www.langsspt.com=-2; \
                    CNZZDATA1259850767=1720412073-1473336634-%7C1474369186; \
                    PHPSESSID=acca33kc0renrrf06isptoshc5'
    }


def test_start():
    global headers
    try:
        test_data = {'username': 'qwhher', 'password': '123456yyy', 'repassword': '123456yyy'}
        test_data_encode = urllib.parse.urlencode(test_data)
        conn = http.HTTPConnection(SERVER_NAME)
        conn.request("POST", URL, test_data_encode, headers)
        result = conn.getresponse()
        if result.status == 200:
            res_body = result.read().decode()
            print(res_body)
        else:
            print('status:', result.status)
        conn.close()
    except Exception as e:
        print(e)

test_start()
