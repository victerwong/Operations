#!/usr/bin/python
# -*- coding: UTF-8 -*-

#    __author__ = 'wanggd'
#    __date__ = '2019/12/11'
#    __Ver.__ = v0.1
#    __Desc__ = 用来定义后台执行

import os,time
from def_sendMail import sendMail
from apscheduler.schedulers.background import BackgroundScheduler

# ##通过参数统一设置文档执行内容：
# ##sendTitl的取值是{dailyFirst,dailySec,dailyThird,month,weekly,weeklyFirst,weeklyChecked,名字无所谓只要匹配即可}:

# #用于测试：
# sendMail('dailyThird')

##构造定时任务：

def schedJob():
    def testSend():
        sendMail('发送测试')
    def dailyFirst():
        sendMail('每日优先估值')
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

    if __name__ == '__main__':
        scheduler = BackgroundScheduler()
        scheduler.add_job(dailyFirst, 'cron', day_of_week='0-4', hour='12', minute='30' )
        scheduler.add_job(dailySec, 'cron', day_of_week='0-4', hour='15', minute='30')
        scheduler.add_job(dailyThird, 'cron', day_of_week='0-4', hour='19', minute='00')
        # scheduler.add_job(dailyThird, 'cron', day_of_week='0-4', hour='17', minute='18')
        scheduler.add_job(weeklyFirst, 'cron', day_of_week='0-4', hour='14', minute='00')
        scheduler.add_job(weeklySec, 'cron', day_of_week='0-4', hour='19', minute='15')
        scheduler.add_job(weeklyThird, 'cron', day_of_week='0-4', hour='19', minute='30')
        scheduler.add_job(month, 'cron', day ='1-9', hour='19', minute='45')

        # 这里的调度任务是独立的一个线程
        scheduler.start()
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        try:
            # 其他任务是独立的线程执行
            while True:
                time.sleep(200)
                print('Waiting!')
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
            print('Exit The Job!')

schedJob()