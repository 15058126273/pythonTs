#   encoding=utf-8

import re
import http.client as http
import urllib

SERVER = 'image.so.com'
URL = '/j'


def get_img(name, page=1):
    param = {'q': name, 'sn': 30, 'pn': 30*page}

    global URL
    URL += '?'+urllib.parse.urlencode(param)
    conn = http.HTTPConnection(SERVER)
    conn.request('GET', URL)
    res = conn.getresponse()
    if res.status == 200:
        data = res.read().decode()
        data = data.replace('false', 'False').replace('null', '').replace(':,', ':').replace(':}', '}')
        all = []
        for img in eval(data).get('list'):
            all.append(img.get('img'))
        result = open('result.txt', 'w')
        result.write(str(all))
        result.close()
        del all
    else:
        print('失败')

get_img('hehe', 2)
