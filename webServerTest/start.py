import threading, time, http.client as httplib, math


# 测试的服务器
SERVER_NAME = "192.168.1.72:8080"
# 需要测试的 url
URL = '/'
# 同时运行的线程数
THREADS_COUNT = 10000
# 每个线程运行多少次
RUN_COUNT = 100
# 开始的时间
START_TIME = time.time()
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
        while i < RUN_COUNT:
            self.test_performance()
            i += 1
        global FINISH_THREAD
        FINISH_THREAD += 1
        if FINISH_THREAD == THREADS_COUNT:
            get_result()

    def test_performance(self):
        conn = httplib.HTTPConnection(SERVER_NAME)
        conn.request("GET", URL)
        res = conn.getresponse()
        if res.status == 200:
            self.success_count += 1
        else:
            self.fail_count += 1
        conn.close()


i = 0
while i < THREADS_COUNT:
    try:
        t = RequestThread("thread" + str(i))
        THREADS.append(t)
        t.start()
        i += 1
        CREATED_THREAD += 1
    except:
        print('无法创建新的线程了，目前已有线程：', CREATED_THREAD, '个')
        THREADS_COUNT = CREATED_THREAD
        break

def get_result():
    time_span = time.time() - START_TIME
    s_count = 0
    f_count = 0
    for t in THREADS:
        s_count += t.success_count
        f_count += t.fail_count
    print("耗时(s):", str(round(time_span, 3)))
    print("成功的请求数(个)：", str(s_count))
    print("失败的请求数(个)：", str(f_count))
    print("平均每秒请求(个)：", str(round(s_count / time_span, 2)))
    print("平均每个请求耗时(秒)：", str(round(time_span / s_count, 5)))

