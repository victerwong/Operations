#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
#    __author__ = 'wanggd'
#    __date__ = '2019/12/11'
#    __Ver.__ = v0.1
#    __Desc__ =

import os,sys,time,threading,configparser
from def_sendMail import sendMail
from apscheduler.schedulers.background import BackgroundScheduler

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

def sched(option):
        day = getSvrOption('SchedulerDay', option)
        hour = getSvrOption('SchedulerHour', option)
        minute = getSvrOption('SchedulerMinute', option)
        scheduler = BackgroundScheduler()
        perTask=lambda option=option:sendMail(option)
        # perTask =lambda option=option:print(option)
        sched=scheduler.add_job(perTask, 'cron', day_of_week=day, hour=hour, minute=minute)
        return sched

def schedJob():
    for option in svr_conf.options('path'):
        try:
            sched(option)
            print(svr_conf.options('path'),option)
        except:
            pass


def bkJob():
    threading.Thread(target=schedJob_thread).start()

def schedJob_thread():
    scheduler = BackgroundScheduler()
    schedJob()
    # 这里的调度任务是独立的一个线程
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        # 其他任务是独立的线程执行
        while True:
            time.sleep(200)
            print('等待执行中．．．')
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print('Exit The Job!')

bkJob()