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


# 抓取代理ip
# capture = captureIp.CaptureIp()
# capture.start()


tidy = tidyIp.TidyIp(False)
print(tidy.checkAll)
