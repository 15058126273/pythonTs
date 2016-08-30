import http.client as httplib


def test_start():
    # 配置conn
    conn = httplib.HTTPConnection('192.168.1.72:8080')
    conn.request('GET', '/')
    res = conn.getresponse()
    if res.status == 200:
        res_body = res.read()
        res_file = open('result.txt', 'wb')
        res_file.write(res_body)
        res_file.close()
    conn.close()

test_start()
