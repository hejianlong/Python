# -*- coding: utf-8 -*-

# @File    : run_spider.py
# @Date    : 2018-08-06
# @Author  : Peng Shiyu

from scrapy import cmdline
import time,datetime
import logging
import os

def start_spider():
    name = 'publict_R，公共资源类信息'
    print(name)
    f = open('../爬虫日志.txt','a',encoding='utf-8')
    f.write('框架启动...'+str(datetime.datetime.now())+ ' ' + name +'\n')
    f.close()
    start = time.time()
    os.system('scrapy crawlall')

if __name__ == '__main__':
    start_spider()