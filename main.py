# -*- coding: utf-8 -*-
from uiautomator import device as d
import time
import os
import sys


# 初始化程序连接
def adb_connect():
    adb_response = os.popen("adb connect 127.0.0.1:7555")
    return adb_response.read()


# 自动翻页
def auto_swipe():
    d.screen.on()  # 点亮屏幕
    d.swipe(500, 500, 0, 500)  # 模拟器坐标位置


# 进度提示，延时
def rep_progress(duration, avg_read_time, pages_count):
    import math
    import random
    # 阅读时间，N（mean=avg_read_time）
    read_time = random.gauss(avg_read_time, 15)
    if read_time < 0 or read_time>avg_read_time+30:
        read_time = avg_read_time
    # 进度条相关
    MAX_LEN = 30
    MAX_TIME = avg_read_time+30
    TIME_SPLIT = math.ceil(MAX_TIME/MAX_LEN)
    time_loop = math.ceil(read_time/TIME_SPLIT)
    time_minus = time_loop*TIME_SPLIT-read_time
    # 总计时间，秒转为 hh：mm：ss
    m, s = divmod(int(duration+read_time), 60)
    h, m = divmod(m, 60)
    for i in range(time_loop):
        sy_1 = "▇" * (i+1)
        sy_2 = ".." * (time_loop-i-1)
        if i == 0:#补齐差值
            time.sleep(time_minus)
        else:
            time.sleep(TIME_SPLIT)
        print('\r正在刷新{:0>3d}页: [{}{}] {:.2f}s | {:02d}:{:02d}:{:02d}'.format(pages_count+1, sy_1, sy_2, read_time, h, m, s), end="")
    print('')


# 输入args1、args2
if __name__ == '__main__':
    sub_page, avg_read_time = sys.argv[1], sys.argv[2]
    start_time, count = time.time(), 0
    status = adb_connect().split(' ')[0]
    if status == 'connected' or status == 'already':
        print('连接成功！开始执行程序！')
    else:
        print('连接失败！程序退出！')
        exit()
    while True:
        if count >= int(sub_page):
            break
        #avg_read_time = 60
        #round(random.uniform(35, 60),2)
        rep_progress(int(time.time() - start_time), int(avg_read_time), count)
        auto_swipe()
        count += 1
