# -*- encoding=utf-8 -*-
"""
    python: 3.5
    time: 2016-09-21
    author: yjy
    describe: 对代理ip操作的主要脚本
"""
import captureIp
import tidyIp
import checkIp


def capture(url, page, pages, save_path, line_size):
    """
    抓取代理ip
    ('http://www.kuaidaili.com/free/inha/_PAGE/', 1, 10, 'checkIp.txt', 1)
    :param url: str 抓取的网页地址页（号用 _PAGE 字符替换）
    :param page: int 起始页号
    :param pages: int 抓取页数
    :param save_path: str 抓取ip存放文件地址
    :param line_size: int 端口号在ip后几行
    :return:
    """
    captureIp.CaptureIp(url, page, pages, save_path, line_size).start()


def tidy(check_all, fail_path, check_path):
    """
    整理ip(去重)
    (False, 'failip.txt', 'checkIp.txt')
    :param check_all: boolean 是否与失效ip比较
    :param fail_path: str 失效ip文件地址
    :param check_path: str 需要整理的ip文件地址
    :return:
    """
    tidyIp.TidyIp(check_all, fail_path, check_path).start()


def check(do_all, create_thread, url, check_path, fail_path):
    """
    代理ip检测
    (False, 40, "http://www.langsspt.com/", 'checkIp.txt', 'failip.txt')
    :param do_all: boolean 是否要测试所有的ip（包括 之前失效的ip）
    :param create_thread: int 计划启动的线程数
    :param url: str 测试地址
    :param check_path: str 测试ip文件地址
    :param fail_path: str 失效ip文件地址
    :return:
    """
    checkIp.CheckIp(do_all, create_thread, url, check_path, fail_path).start()


# capture('http://www.kuaidaili.com/free/inha/_PAGE/', 1, 10, 'checkIp.txt', 1)
#
check(False, 50, "http://www.langsspt.com/", 'ip.txt', 'failip.txt')

tidy(True, 'failip.txt', 'ip.txt')
