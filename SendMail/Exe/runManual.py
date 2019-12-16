#!/usr/bin/python
# -*- coding: UTF-8 -*-

#    __author__ = 'wanggd'
#    __date__ = '2019/12/11'
#    __Ver.__ = v0.1
#    __Desc__ = 用来定义一个执行窗口


import os,time,sys,configparser
import tkinter as tk
import tkinter.messagebox
from def_sendMail import sendMail
from runBackground import schedJob

# ##通过参数统一设置文档执行内容：
# ##sendTitl的取值是{dailyFirst,dailySec,dailyThird,month,weekly,weeklyFirst,weeklyed,名字无所谓只要匹配即可}:

# ##sendTitl的取值是{每日优先估值,每日提前推送,每日,每月,每周提前,每周已核对,每周,名字无所谓只要匹配即可}:

# #用于{每日优先估值}：
# sendMail('dailyFirst')
#
# #用于{每日提前推送}：
# sendMail('dailySec')
#
# #用于{每日}：
# sendMail('dailyThird')
#
# #用于{每月}：
# sendMail('month')
#
# #用于{每周提前}：
# sendMail('weeklyFirst')
#
# #用于{每周已核对}：
# sendMail('weeklyed')
#
# #用于{每周}：
# sendMail('weekly')

# #用于测试：
#
# sendMail('发送测试')


#获取程序运行目录的父目录:
def abspath():
    # cur_path = os.path.dirname(os.path.realpath(__file__))    #这里是获取当前路径的办法
    abspath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 这里是获取当前路径的父路径
    return abspath

# 设定配置文件：
svr_path = os.path.join(abspath(), 'Conf\svrcfg.ini')
# 读取设置的配置文件：
svr_conf = configparser.ConfigParser()
svr_conf.read(svr_path, encoding='utf-8-sig')

#
btn1=svr_conf.options('path')[0]
btn2=svr_conf.options('path')[1]
btn3=svr_conf.options('path')[2]
btn4=svr_conf.options('path')[3]
btn5=svr_conf.options('path')[4]
btn6=svr_conf.options('path')[5]
btn7=svr_conf.options('path')[6]
btn8=svr_conf.options('path')[7]

btn88='开启后台计划'
btn99='停止运行'

# 第1步，实例化object，建立窗口window
window = tk.Tk()

# 第2步，给窗口的可视化起名字
window.title('自动发邮件程序')

# 第3步，设定窗口的大小(长 * 宽)
window.geometry('500x350')  # 这里的乘是小x

# 第4步，在图形界面上创建一个标签label用以显示并放置
l = tk.Label(window, bg='yellow', width=20, text='请选择要执行的任务：')
l.pack()


# 第6步，定义触发函数功能

direction1=['left','right','center']
direction2=['top','bottom' , 'left', 'right']

def dailyFirst():
    sendMail('每日优先估值')
    # tkinter.messagebox.showinfo()
def dailySec():
    sendMail('每日提前推送')

def dailyThird():
    sendMail('每日')

def weeklyFirst():
    sendMail('每周提前')

def weeklySec():
    sendMail('每周已核对')

def weeklyThird():
    sendMail('每周')

def month():
    sendMail('每月')

def testSend():
    sendMail('发送测试')

try:
    c1 = tk.Button(window, text=btn1, bg='green',command=dailyFirst)  # 传值原理类似于radioButton部件
    c1.pack()
    c2 = tk.Button(window, text=btn2, bg='green',command=dailySec)
    c2.pack()
    c3 = tk.Button(window, text=btn3, bg='green',command=dailyThird)
    c3.pack()
    c4 = tk.Button(window, text=btn4, bg='yellow',command=weeklyFirst)
    c4.pack()
    c5 = tk.Button(window, text=btn5, bg='yellow',command=weeklySec)
    c5.pack()
    c6 = tk.Button(window, text=btn6, bg='yellow',command=weeklyThird)
    c6.pack()
    c7 = tk.Button(window, text=btn7, bg='red',command=month)
    c7.pack()
    c8 = tk.Button(window, text=btn8,bg='green',command=testSend)
    c8.pack(side='left')
    c88 = tk.Button(window, text=btn88, bg='red',command=schedJob)
    c88.pack(side='right')
    c99 = tk.Button(window, text=btn99, bg='red',justify='left',command=SystemExit)
    c99.pack(side='bottom')
except:
    pass

# 第7步，主窗口循环显示
window.mainloop()
