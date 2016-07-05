#-*- coding:utf-8 -*-
import linecache
import time
import ConfigParser
import string, os, sys
import re

# latest_path = 'logs/latest.log'
cf = ConfigParser.ConfigParser()     #实例化
cf.read('first_instruction.conf')    #读取配置文件

global last_linage
last_linage = 0    #默认过去行数
check_wait = 0

def check_info(info):    #统计消息
    if str(cf.get("basis","statistics ")) == "True":    #判断功能是否开启
        pass

while True:
    time.sleep(1)
    file_object = open(str(cf.get("server","server-side_latest_path")))

    # print "Done."
    linage = len(open(str(cf.get("server","server-side_latest_path")),'rU').readlines())    #获取文件行数
    # print linage

    while linage != last_linage:   #如果新旧不吻合
        last_linage = last_linage+1    #下一行号
        linecache.clearcache()   #清理linecache缓存
        the_line=linecache.getline(cf.get("server","server-side_latest_path"),last_linage)   #扫描下一行内容
        print "[Server Info "+str(last_linage)+"]",the_line
