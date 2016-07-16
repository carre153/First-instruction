#-*- coding:utf-8 -*-
import os
def stop():
    exit()

def output(text):
    print text

def reboot():
    try:
        ask = raw_input('此举动会杀掉Java的任何进程，你真的要这么做吗？[1:yes,2:NO]')
        if ask == 1:
            os.system('taskkill /F /IM java.exe')
            print '进程已被销毁.'
    except:
        print '进程销毁失败'