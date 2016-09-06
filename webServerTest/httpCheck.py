#
# Python Version: 3.5
# 运行该项目需保证测试的服务器能连接
#
#
import threading
import time
import http.client as http


# 测试的服务器 + 端口 （有些大网站会认定你是攻击并且重置你的请求，比如baidu.com）
SERVER_NAME = "www.langsspt.com"
# 访问的页面
# URL = '/404.html'
URL = '/index.php/Index/msgSend'
# 同时运行的线程数 （每个电脑能开的线程数不同（我：893个线程），如果超过了系统的最大负荷，则只创建能创建的最大线程数）
THREADS_COUNT = 800
# 每个线程执行多少次connect
RUN_COUNT = 1000

# 开始的时间
START_TIME = 0
# 线程池
THREADS = []
# 已完成的线程数
FINISH_THREAD = 0
# 已创建的线程数
CREATED_THREAD = 0


# 创建一个 threading.Thread 的派生类
class RequestThread(threading.Thread):
    # 构造函数
    def __init__(self, thread_name):
        threading.Thread.__init__(self)
        self.success_count = 0
        self.fail_count = 0

    # 线程运行的入口函数
    def run(self):
        i = 0
        try:
            while i < RUN_COUNT:
                self.test_performance()
                i += 1
        except:
            pass
        global FINISH_THREAD, THREADS_COUNT
        FINISH_THREAD += 1
        if FINISH_THREAD == THREADS_COUNT:
            get_result()

    # 链接测试服务器
    def test_performance(self):
        conn = http.HTTPConnection(SERVER_NAME)
        conn.request("GET", URL)
        res = conn.getresponse()
        if res.status == 200:
            self.success_count += 1
        else:
            self.fail_count += 1
        conn.close()


# 测试完毕后统计结果
def get_result():
    time_span = time.time() - START_TIME
    s_count = 0
    f_count = 0
    for t in THREADS:
        s_count += t.success_count
        f_count += t.fail_count
    print("耗时(s):", str(round(time_span, 3)))
    print("总请求数(个)：", str(CREATED_THREAD*RUN_COUNT))
    print("成功的请求数(个)：", str(s_count))
    print("失败的请求数(个)：", str(f_count))
    print("平均每秒请求(个)：", str(round(s_count / time_span, 2)))
    print("平均每个请求耗时(秒)：", str(round(time_span / s_count, 5)))


try:
    START_TIME = time.time()
    while THREADS_COUNT > 0:
        t = RequestThread("thread" + str(THREADS_COUNT))
        THREADS.append(t)
        t.start()
        THREADS_COUNT += -1
        CREATED_THREAD += 1
except:
    print('无法创建新的线程了，目前已有线程：', CREATED_THREAD, '个')
finally:
    THREADS_COUNT = CREATED_THREAD
    print(time.strftime('%Y-%m-%d %H:%M:%S'), ':', '正在试探', SERVER_NAME, '啦啦啦....')
