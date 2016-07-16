#-*- coding:utf-8 -*-

import os,sys
import thread
import linecache
import time
import ConfigParser
import re
import logging
import smtplib
import urllib
import base64

import fi_library.system

import fi_library
from fi_library import *

cf = ConfigParser.ConfigParser()     #载入配置文件
cf.read('first_instruction.conf')
ISODATEFORMAT = '%Y-%m-%d_%H-%M' #当前日期

if cf.get('developer','simple_log') == 'True':    #判断需要日志类型
    format='[%(asctime)s] [%(levelname)s] %(message)s'
else:
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'

logging.basicConfig(level=logging.DEBUG,    #载入日志
                format=format,
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='fi_bin/logs/'+ str(time.strftime( ISODATEFORMAT, time.localtime()) + '.log'),
                filemode='w')

#将INFO级别或更高的 日志信息打印到标准错误
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [First instruction/%(levelname)s]: %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


last_linage = 0    #默认过去行数
check_wait = 0

######

def updata():
    if int(bool(cf.get('basis','auto_updata'))) == True:  #检查是否开启自动更新
        updata_info = urllib.urlopen(str(cf.get('developer','check_updata_url'))).readline() #遍历
        '''实例化消息'''

        url = ''.join(re.findall('<url>(.*?)<url/>',updata_info))
        if ''.join(re.findall('<version>(.*?)<version/>',updata_info)) != base64.b64decode(cf.get('developer','number')): #对比现版本与原版本
            pass
        else:
            pass
    else:
        pass


def send_mail(title,info):   #邮件发送
    if str(cf.get('basis','mail_send')) == 'True':
        to='carre1@yeah.net;'
        text='''
        <html>
        <body>
        <p>
            <h1>First-instruction 通知 - %s</h1>
            <hr>
            %s
        </p>
        </body>
        </html>
        '''%(title,info)
        try:
            server = smtplib.SMTP_SSL()
            server.connect(str(cf.get('send_mail','smtp_server')), int(cf.get('send_mail','smtp_port')))
            server.login(str(cf.get('send_mail','smtp_user')),str(cf.get('send_mail','smtp_psw')))
            msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\nContent-Type:text/html\r\n\r\n%s"% (str(cf.get('send_mail','smtp_user')), str(cf.get('send_mail','to')),title,text)) #组装信头
            server.sendmail(str(cf.get('send_mail','smtp_user')), to, msg)
            logging.info('成功发送信件: \n================================================\n'+msg+'\n================================================')
        except:
            logging.error('不能成功地发送通知，请检查配置是否正确。')
    else:
        pass

def statistical(info):    #统计消息
    if str(cf.get("basis","statistics")) == "True":    #判断功能是否开启
        def s_startserver():    #开启服务器记录
            try:
                records_file = open('fi_bin/statistical_records/start_server.txt','r')
                read_records_file = records_file.read()    #读取统计记录文件
                records_file.close()
                output_records = int(read_records_file)+1
                output = open('fi_bin/statistical_records/start_server.txt', 'w')    #写入
                output.write(str(output_records))
                output.close()
                send_mail('First-instruction 侦测到服务器开启','First-instruction侦测到服务器被开启，请注意是否自行操作。')
            except:
                logging.error('Log message failed.Please confirm that fi_bin/statistical_records/start_server.txt is a number')

        def s_closeserver():    #关闭服务器记录
            try:
                records_file = open('fi_bin/statistical_records/close_server.txt','r')
                read_records_file = records_file.read()    #读取统计记录文件
                records_file.close()
                output_records = int(read_records_file)+1
                output = open('fi_bin/statistical_records/close_server.txt', 'w')    #写入
                output.write(str(output_records))
                output.close()
                send_mail('First-instruction侦测到服务器关闭','First-instruction侦测到服务器被关闭，请注意是否自行操作。')
            except:
                logging.error('Log message failed.Please confirm that fi_bin/statistical_records/close_server.txt is a number')

        def s_player_up():    #玩家上线记录
            try:
                records_file = open('fi_bin/statistical_records/player_up.txt','r')
                read_records_file = records_file.read()    #读取统计记录文件
                records_file.close()
                output_records = int(read_records_file)+1
                output = open('fi_bin/statistical_records/player_up.txt', 'w')    #写入
                output.write(str(output_records))
                output.close()
            except:
                logging.error('Log message failed.Please confirm that fi_bin/statistical_records/player_up.txt is a number')

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
                logging.error('Log message failed.Please confirm that fi_bin/statistical_records/command.txt is a number')

        d_info = re.search(r"(?<=]: ).+?(?=$)",info,re.M)

        try:
            if d_info.group(0) == 'Timings Reset':
                s_startserver()
            elif d_info.group(0) == 'Stopping server':
                s_closeserver()
            else:
                pass

            if str(re.search(r'\sSet own game mode to\s', d_info.group(0)).group(0)):
                pass
            else:
                send_mail('侦测到玩家更改模式','我们侦测到玩家正在更改模式，详细信息为：'+d_info.group(0))
        except:
            pass

    s_server_command()    #记录消息数量

'''System'''
def stop():
    exit()

def output(text):    #
    print text

def output():    #
    print '\n'

def reboot():
    try:
        print '此举动会杀掉Java的任何进程，你真的要这么做吗？[1:yes,2:NO]'
        ask = raw_input('>>>')
        if ask == '1':
            os.system('taskkill java.exe')
    except:
        print '进程销毁失败'

'''============Main============'''

def main(last_linage):
    send_mail('First-instruction已启动','First-instruction已经被启动。感谢你的使用。')    #启动通知
    updata()
    while True:
        time.sleep(1)
        file_object = open(str(cf.get("server","server-side_latest_path")))   #目标文件位置

        linage = len(open(str(cf.get("server","server-side_latest_path")),'rU').readlines())    #获取文件行

        while linage != last_linage:   #如果新旧不吻合
            last_linage = last_linage+1    #下一行号
            linecache.clearcache()   #清理linecache缓存
            the_line=linecache.getline(cf.get("server","server-side_latest_path"),last_linage)   #扫描下一行内容
            # print "[Server Info "+str(last_linage)+"]",the_line
            statistical(the_line)    #加入统计

def shell():
    print str(cf.get('basis','welcome_info')),' By:Fadedsky Team (http://www.fadedsky.cc)'
    while True:
        command = raw_input('>>> ')
        affair(command)

def affair(command):    #事务
    commands = {
        'stop':'stop()',    #停止
        'output':'output()',    #打印字符串到控制台
        'reboot':'reboot()',    #重启服务端
    }
    try:
        implement = commands[str(command)]
    except:
        print '[Error]The command is not valid. Please check your spelling.'

    try:
        eval(implement)
    except:
        print '[Error]An error occurred while running'

def run(last_linage):

    logging.info('The First_instruction are start.')
    thread.start_new_thread(shell, ())   #创建外壳线程
    time.sleep(1)
    main(last_linage)    #主线程

if __name__ == '__main__':
    run(last_linage)
