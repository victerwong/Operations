#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
#    __author__ = 'wanggd'
#    __date__ = '2019/12/11'
#    __Ver.__ = v0.1
#    __Desc__ = 用来定义一个执行窗口;增加了动态生成菜单的功能年.


import os,threading,sys,configparser
import tkinter as tk
from def_sendMail import sendMail
from decompressFiles import doCompRar
from writerarconf import writeConf
# from runBackground import bkJob

#获取程序运行目录的父目录:
def abspath():
    # cur_path = os.path.dirname(os.path.realpath(__file__))    #这里是获取当前路径的办法
    abspath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 这里是获取当前路径的父路径
    return abspath

# 设定配置文件：
svr_path = os.path.join(abspath(), 'Conf\svrcfg.ini')
# svr_path=r'C:\SendMail\Conf\svrcfg.ini'
# 读取设置的配置文件：
svr_conf = configparser.ConfigParser()
svr_conf.read(svr_path, encoding='utf-8-sig')

def getSvrOption(section, option):
    try:
        getSvrOption = svr_conf.get(section, option)
        return getSvrOption
    except:
        print('[svrcfg.ini]字典设置有误，请检查或修正后再运行。')
        sys.exit()

parent_path = getSvrOption('rarfile', 'parent_path')

nameList=svr_conf.options('path')
nameLen=len(nameList)

#构建四组列表，供后续界面分组：
nameListDay=[]
nameListWeek=[]
nameListMonth=[]
nameListOther=[]
#按名字做分为四组列表：
for name in nameList:
    # print(name)
    if '每日'in name:
        nameListDay.append(name)
    elif '每周' in name:
        nameListWeek.append(name)
    elif '每月' in name:
        nameListMonth.append(name)
    else:
        nameListOther.append(name)


def tkbtn(fm,list):
    for btn in list:
        ##command指令对接的方法，不用lambda，则会立即执行，用了lambda，则会固话for循环的最后一个值，使用lambda name=name：def(name),来动态匹配
        tk.Button(fm,text=btn,command=lambda btn=btn:sendMail(btn)).pack(side='left', fill='x', expand='yes')
    return tk.Button


class App:
    def __init__(self, master):
        self.master = master
        self.initWidgets()

    def initWidgets(self):
        # 创建第一个容器
        fm1 = tk.Frame(self.master)
        # 该容器放在左边排列
        fm1.pack(side='top', fill='both', expand='yes')
        tk.LabelFrame(fm1, bg='green', width=20, text='每日任务列表：')
        # 设置按钮从顶部开始排列，且按钮只能在垂直（X）方向填充
        tkbtn(fm1,nameListDay)

        fm2 = tk.Frame(self.master)
        fm2.pack(side='top', fill='both', expand='yes')
        tk.Label(fm2, bg='green', width=20, text='每周任务列表：')
        tkbtn(fm2, nameListWeek)

        fm3 = tk.Frame(self.master)
        fm3.pack(side='top', fill='both', expand='yes')
        tk.Label(fm3, bg='green', width=20, text='每月任务列表：')
        tkbtn(fm3, nameListMonth)

        fm4 = tk.Frame(self.master)
        fm4.pack(side='top', fill='both', expand='yes')
        tk.Label(fm4, bg='green', width=20, text='其他任务列表：')
        tkbtn(fm4, nameListOther)

        fm5 = tk.Frame(self.master)
        fm5.pack(side='top', fill='both', expand='yes')
        # tk.Button(fm5, text='开启计划', command=schedJob).pack(side='left', fill='x', expand='yes')
        tk.Button(fm5, text='生成配置文件（rarcfg）', command=lambda: writeConf(r'D:\Codes\unZip','rartype')).pack(side='left', fill='x', expand='yes')
        tk.Button(fm5, text='解压缩（测试）', command=lambda :doCompRar()).pack(side='left', fill='x', expand='yes')

        fm6 = tk.Frame(self.master)
        fm6.pack(side='top', fill='both', expand='yes')
        tk.Button(fm6, text='退出程序', command=exit).pack(side='left', fill='x', expand='yes')

def main():
    threading.Thread(target=gui_thread).start()


def gui_thread():
    root = tk.Tk()
    root.title("自动发邮件-手动补发程序")
    app = App(root)
    root.mainloop()

main()