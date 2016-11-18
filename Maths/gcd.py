# -*- encoding=utf-8 -*-
"""
    python: 3.5
    author: yjy
    time: 2016-11-18
    desc: 取两个整数的最大公约数
"""
import random
import time
import math


def invoke_gcd(target):
    """
    公共函数块
    :param target:
    :return:
    """
    a = random.randint(0, 100000)
    b = random.randint(0, 100000)
    time.clock()
    print(a, "与", b, "的最大公约数为：")
    print(target.gcd(10, 5), "耗时：", round(time.clock(), 6))


class GcdD:
    """
    普通循环法
    """
    def __init__(self):
        invoke_gcd(self)

    def gcd(self, a, b):
        if a == 0 or b == 0:
            return 0
        i = 1
        g = 1
        while i < a and i < b:
            if a % i == 0 and b % i == 0:
                g = i
            i += 1
        else:
            return g


class GcdZ:
    """
    辗转相除法
    """
    def __init__(self):
        invoke_gcd(self)

    def gcd(self, a, b):
        if a == 0 or b == 0:
            return 0
        c = a % b
        if c == 0:
            return b
        else:
            return self.gcd(b, c)


class GcdG:
    """
    更相减损术
    """
    def __init__(self):
        invoke_gcd(self)

    def gcd(self, a, b):
        if a <= 0 or b <= 0:
            return 0
        t = 1
        while 1:
            if a % 2 == 0 and b % 2 == 0:
                a /= 2
                b /= 2
                t *= 2
            elif (a - b) > 0:
                a -= b
            elif (a - b) < 0:
                b -= a
            else:
                return t*a


GcdG()


