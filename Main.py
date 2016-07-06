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

def statistical(info):    #统计消息
    if str(cf.get("basis","statistics")) == "True":    #判断功能是否开启
        def s_startserver():    #开启服务器记录
            records_file = open('fi_bin/statistical_records/start_server.txt','r')
            read_records_file = records_file.read()    #读取统计记录文件
            records_file.close()
            output_records = int(read_records_file)+1
            output = open('fi_bin/statistical_records/start_server.txt', 'w')    #写入
            output.write(str(output_records))
            output.close()

        def s_closeserver():    #关闭服务器记录
            records_file = open('fi_bin/statistical_records/close_server.txt','r')
            read_records_file = records_file.read()    #读取统计记录文件
            records_file.close()
            output_records = int(read_records_file)+1
            output = open('fi_bin/statistical_records/close_server.txt', 'w')    #写入
            output.write(str(output_records))
            output.close()

        def s_player_up():    #玩家上线记录
            records_file = open('fi_bin/statistical_records/player_up.txt','r')
            read_records_file = records_file.read()    #读取统计记录文件
            records_file.close()
            output_records = int(read_records_file)+1
            output = open('fi_bin/statistical_records/player_up.txt', 'w')    #写入
            output.write(str(output_records))
            output.close()

        def s_server_command():
            try:
                records_file = open('fi_bin/statistical_records/command.txt','r')
                read_records_file = records_file.read()    #读取统计记录文件
                records_file.close()
                output_records = int(read_records_file)+1
                output = open('fi_bin/statistical_records/command.txt', 'w')    #写入
                output.write(str(output_records))
                output.close()
            except:
                print '[Fi Error] Not Can Cannot write command.txt '

        d_info = re.search(r"(?<=]: ).+?(?=$)",info,re.M)

        try:
            # print "Fi Info : ",str(d_info)
            if d_info.group(0) == 'Timings Reset':
                print 'Timings Reset'
            elif d_info.group(0) == 'Stopping server':
                print 'Server stop'
            else:
                pass
        except:
            pass

    s_server_command()    #记录消息数量

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
        statistical(the_line)    #加入统计