#-*- coding:utf-8 -*-
import linecache
import time

#导入配置文件
file_path = 'logs/latest.log'

global last_linage    #默认过去行数
last_linage = 0

def check_status(info):
    print "done"

while True:
    time.sleep(1)
    file_object = open(file_path)

    # print "Done."
    linage = len(open(file_path,'rU').readlines())    #获取文件行数
    # print linage

    while linage != last_linage:   #如果新旧不吻合
        last_linage = last_linage+1    #下一行号
        linecache.clearcache()   #清理linecache缓存
        the_line=linecache.getline(file_path,last_linage)   #扫描下一行内容
        print "[Server Info "+last_linage+"]",the_line
