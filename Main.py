#-*- coding:utf-8 -*-

import linecache
import time
import ConfigParser
import re
import logging
import smtplib

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


global last_linage
last_linage = 0    #默认过去行数
check_wait = 0

logging.info('The First_instruction are start.')

######

def send_mail(title,info):   #邮件发送
    if str(cf.get('basis','mail_send')) == 'True':
        to='carre1@yeah.net;'
        text='''
        <html>
        <body>
        <p>
            <h1>First-instruction 通知</h1>
            <hr>
            %s
        </p>
        </body>
        </html>
        '''%(info)
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
            # print "Fi Info : ",str(d_info)
            if d_info.group(0) == 'Timings Reset':
                s_startserver()
            elif d_info.group(0) == 'Stopping server':
                s_closeserver()
            else:
                pass
        except:
            pass

    s_server_command()    #记录消息数量


send_mail('First-instruction已启动','First-instruction已经被启动。感谢你的使用。')    #启动通知

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
