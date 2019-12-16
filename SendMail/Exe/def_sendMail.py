#!/usr/bin/python
# -*- coding: UTF-8 -*-

#    __author__ = 'wanggd'
#    __date__ = '2019/11/27-2019/12/11'
#    __Ver.__ = v0.8
#    __Desc__ = '''
#    自行编写发送邮件程序，以解决母公司软件无法修改发件人、正文等问题；
#    0.1版本主要构建程序主框架，测试能否解决预期目标；
#    0.2版本主要通过用例，完成内部发送功能的测试，主要确定程序框架，并将发送接口由sendmail修改为sendmessage，以解决无法抄送的问题；
#    0.3版本主要完善相关功能，根据关键词匹配附件，自动生成邮件标题及正文，并增加无附件不发送邮件功能，
#    0.4版本做了简单重构，将程序修改为读取配置文件，同时增加了日志记录的问题；
#    0.5版本主要完善了pop客户端无法识别文件名，以及QQ邮箱中文乱码的问题；增加了抄送、密抄为空的对应处理；
#    0.6版本主要想重构以匹配邮件发送的各种分类问题；
#    0.7版本，在程序完成确认前，增加程序完成后，自动给指定人员（可能放在server配置中），发送执行记录的功能。
#    0.8版本：自动备份文件到压缩包，删除目录树并重新生成；该操作主要配合后续每日调度，避免发送重复的附件。
#               '''

def sendMail(sendTitle):

    import os,time,sys, shutil,zipfile,smtplib,configparser
    from email.header import Header             ##使用Header函数，主要解决旧版本客户端无法识别附件名的问题。
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.application import MIMEApplication

    ###---------------本段填写运行参数-----------------------：

    sendTitle= sendTitle
    ###-----------------------------------------------------:
    msg_zt = ''
    msg_zw = ''
    ###---------------本段是一些可能用的到参数----------------：
    today = time.strftime('%y%m%d')
    now = time.strftime('%H%M%S')
    nyrdate=time.strftime('%y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
    ###--------------本段设置服务器相关信息-------------------：

    #获取程序运行目录的父目录:
    def abspath():
        # cur_path = os.path.dirname(os.path.realpath(__file__))    #这里是获取当前路径的办法
        abspath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))   #这里是获取当前路径的父路径
        return abspath

    #设定配置文件：
    svr_path = os.path.join(abspath(), 'Conf\svrcfg.ini')
    msg_path =os.path.join(abspath(),'Conf'+'\\'+sendTitle+'.ini')
    #读取设置的配置文件：
    svr_conf = configparser.ConfigParser()
    svr_conf.read(svr_path, encoding='utf-8-sig')
    msg_conf = configparser.ConfigParser()
    msg_conf.read(msg_path, encoding='utf-8-sig')

    ###生成邮件服务器参数：
    ##读svrcfg.ini文件：
    def getSvrOption(section,option):
        try:
            getSvrOption= svr_conf.get(section, option)
            return getSvrOption
        except:
            print('[svrcfg.ini]字典设置有误，请检查或修正后再运行。')
            sys.exit()

    ##读邮件的ini文件：
    def getMsgOption(section,option):
        try:
            getMsgOption= msg_conf.get(section, option)
            return getMsgOption
        except:
            print('发送字典的设置有误，请检查或修正后再运行。')
            sys.exit()
    ##创建目录：
    def mkdir(path):
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在(返回True、False)
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            os.makedirs(path)
            return True
        else:
            return False

    #按照配置文件生成目录：
    def csh():
        #遍历每一个目录：
        try:
            for option in svr_conf.options('path'):
                mkpath=getSvrOption('path',option)
                ##初始化目录：
                mkdir(mkpath)
        except:
            print('目录初始化失败')
            sys.exit()
    csh()
    ##压缩内容：
    def zipDir(dirpath, outFullName):
        z = zipfile.ZipFile(outFullName, 'w', zipfile.ZIP_DEFLATED)
        for dir_path, dir_names, file_names in os.walk(dirpath):
            f_path = dir_path.replace(dirpath, '')  # 这一句很重要，不replace的话，就从根目录开始复制
            f_path = f_path and f_path + os.sep or ''  # 实现当前文件夹以及包含的所有文件的压缩
            for filename in file_names:
                z.write(os.path.join(dir_path, filename), f_path + filename)
        z.close()
        return outFullName

    ##判断获取是否成功：
    def isexit(content):
        try:
            if content != '' and content !=None:
                isexit=content
                return isexit
        except:
            print('[svrcfg]节点设置不正确，请检查或修正后再运行。')
            sys.exit()
    ##生成接收人或接收人列表：
    def islist(content):
        if isinstance(content, list):
            content = ','.join(content)
        else:
            content = content
        return content

    #生成邮件服务器配置信息：
    mailServer =isexit(getSvrOption('server','mailserver'))
    userName =isexit(getSvrOption('server','username'))
    passWord = isexit(getSvrOption('server','password'))
    attPath=isexit(getSvrOption('path',sendTitle))
    #生成密抄对象：{仅在测试阶段供观察使用}
    bcc=isexit(islist(getSvrOption('bcc','bcc')))

    ##--------------本段循环产生数据-------------------------：
    for section in msg_conf.sections():
        msg = MIMEMultipart('mixed')
        # '''
        # 一些资料：
        # 常见的multipart类型有三种：multipart/alternative, multipart/related和multipart/mixed。
        # 邮件类型为"multipart/alternative"的邮件包括纯文本正文（text/plain）和超文本正文（text/html）。
        # 邮件类型为"multipart/related"的邮件正文中包括图片，声音等内嵌资源。
        # 邮件类型为"multipart/mixed"的邮件包含附件。向上兼容，如果一个邮件有纯文本正文，超文本正文，内嵌资源，附件，则选择mixed类型。
        # '''
        msg['From'] = userName
        msg['To'] = isexit(islist(getMsgOption(section,'rcv')))
        msg['cc'] =isexit(islist(getMsgOption(section,'cc')))


        #当不使用密送时注释掉：
        if sendTitle =='testSend' or sendTitle == None or sendTitle == '':
            msg['bcc']=''
        else:
            msg['bcc']=bcc

        # msg['To']= 'wangguodong@galaxycapital.com.cn'
        fileName = isexit(getMsgOption(section,'filename'))

        ##创建并记录发送结果：
        sendRecoder = open(abspath() + '\Result\\'+sendTitle+'_' +today+'.txt', 'a+')
        sendSucces = open(attPath+'\sendSucces.txt', 'a+')          ##txt文件名，请务必与ini文件中的设置保持一致。

        print('\n' + '===============' + '开始记录日志' + '(' + today + ')：' + '===============', file=sendRecoder)
        print('1.发件人： ' + userName, file=sendRecoder)
        print('2.收件人： ' + getMsgOption(section,'rcv'), file=sendRecoder)
        print('3.抄送： ' + getMsgOption(section, 'cc'), file=sendRecoder)
        print('4.附件目录： ' + attPath, file=sendRecoder)
        print('5.附件关键词： ' + fileName, file=sendRecoder)

        ##构建计数器：
        nofiles = 0
        count = 0
        for file in os.listdir(attPath):  # file 表示的是文件名
            count = count + 1

        ##按照ini中定义的关键词，遍历目录：
        for item in os.listdir(attPath):
            itemPath = os.path.join(attPath, item)
            if fileName in item:
                xlsxpart = MIMEApplication(open(itemPath, 'rb').read())
                xlsxpart["Content-Type"] = 'application/octet-stream'
                xlsxpart.add_header('Content-Disposition', 'attachment', filename=Header(os.path.basename(itemPath),'utf-8').encode())
                msg.attach(xlsxpart)

                print('6.附件： ' + itemPath, file=sendRecoder)

                #设定邮件主题：
                if '估值' in item:
                    msg_zt = fileName + '估值表'
                elif '净值' in item:
                    msg_zt = fileName + '净值表'
                elif 'send'in item:
                    msg_zt = '执行情况汇总'
                else:
                    msg_zt = '银河资本净值表'

                ##设定正文内容：
                if msg_conf.has_option(section, 'zw') == True and msg_conf.get(section, 'zw') != '' and msg_conf.get(section, 'zw') != None:
                    msg_zw = msg_conf.get(section, 'zw')
                else:
                    if sendTitle == '每日优先估值' or sendTitle =='发送测试':
                        msg_zw = '您好，附件中是'+ nyrdate + msg_zt + '，请查收。\n尚未与托管行核对，供参考，请知悉。'
                    elif sendTitle =='每日' :
                        msg_zw = '您好，附件中标“未核对”的为未与托管行核对，请知悉。'
                    elif sendTitle =='每周已核对':
                        msg_zw = '您好，附件中是'+ nyrdate + msg_zt + '，已与托管行核对一致，请查收。'
                    else:
                        msg_zw='您好！\n请查收'
            else:
                nofiles = nofiles + 1

    ###--------------本段发送邮件-----------------------------：
        try:
            ##如果附件不为空，则发送邮件：
            if nofiles < count:

                msg['Subject'] = Header(msg_zt, 'utf-8')
                print('7.正文： ' + msg_zw, file=sendRecoder)
                msg_zw = MIMEText(msg_zw, 'plain', 'utf-8')
                msg.attach(msg_zw)

                client = smtplib.SMTP()
                client.connect(mailServer)
                client.login(userName, passWord)
                # sendmail对多收件人支持不好，暂时没解决，使用send_message替代。
                # client.sendmail(sender, rcvall, msg.as_string())
                client.send_message(msg)
                client.quit()
                print('8.发送结果：' + '邮件成功发送！', file=sendRecoder)
                print('===================' + '完成日志记录：' + '===================' + '\n\n', file=sendRecoder)
                print(nyrdate+'_邮件主题：'+msg_zt + '_在：'+now+ '_发送----成功！', file=sendSucces)
                sendSucces.close()
                ##如果成功发送，则15秒后发送下一封邮件：
                time.sleep(15)
            else:
                print('101.附件：' + '未匹配到附件，发送失败，请检查附件或关键词。', file=sendRecoder)
                print('===================' + '完成日志记录：' + '===================' + '\n\n', file=sendRecoder)
                sendFaile = open(attPath + '\sendFaile.txt', 'a+')  ##txt文件名，请务必与ini文件中的设置保持一致。
                print(nyrdate + '_邮件主题：' + fileName + '_在：' + now + '_发送----失败（未匹配到附件）！', file=sendFaile)
                sendFaile.close()
        #创建异常的相关记录：
        except Exception as e:
            print('102.发送结果：发送异常，请检查相关配置（如网络连接状态、发送间隔等）.', file=sendRecoder)
            print(e, file=sendRecoder)
            print('===================' + '完成日志记录：' + '===================' + '\n\n', file=sendRecoder)
            ##txt文件名，请务必与ini文件中的设置保持一致。
            sendFaile = open(attPath+'\sendFaile.txt', 'a+')
            print(nyrdate+'_邮件主题：'+msg_zt + '_在：'+now+ '_发送----失败(异常)！', file=sendFaile)
            sendFaile.close()



    ##压缩目录：
    zipPath=getSvrOption('zipPath','zipPath')
    zipToday=zipPath+'\\'+today
    mkdir(zipToday)
    zipDir(attPath, zipToday+'\\'+sendTitle+now+'.zip')
    ##删除目录：
    shutil.rmtree(attPath)
    time.sleep(5)

    ##重新创建目录，以供后续传入文件：
    csh()

    return sendMail
