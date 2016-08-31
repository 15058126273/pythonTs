import http.client as httplib


def test_start():
    # 配置conn
    conn = httplib.HTTPConnection('www.baidu.com:80')
    conn.request('GET', '/')
    print('sssss')
    res = conn.getresponse()
    print('fffff')
    if res.status == 200:
        res_body = res.read()
        res_file = open('result.txt', 'wb')
        res_file.write(res_body)
        res_file.close()
    else:
        print('status:', res.status)
    conn.close()

test_start()
