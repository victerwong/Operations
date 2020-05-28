#!/usr/bin/python
# -*- coding: UTF-8 -*-

#    __author__ = 'wanggd'
#    __date__ = '2019/11/27-2019/12/11'
#    __Ver.__ = v0.8
#    __Desc__ = 1.遍历指定父目录产生子目录列表；2.人工确认有效的子目录名字（不需要标为0）；3.按目录名分类执行策略；4.根据目录名及策略，执行解压缩流程，并备份压缩包至指定目录；5.上述工作合并为一个工作项，并按照指定时间执行。

import os,time,shutil,configparser
from unrar import rarfile

def doCompRar():
    rar_path = r'D:\Codes\unZip\temp'
    savePath = r'D:\Codes\unZip\unZip'

    file_flag = '.rar'
    today = time.strftime('%y%m%d')
    now = time.strftime('%H%M%S')

    ##初始化目录：
    def csh(dir):
        if os.path.exists(dir) == True and os.path.isdir(dir) == True:
            pass
        else:
            os.mkdir(dir)

    # 生成备份目录及日志目录
    csh(savePath)
    csh(savePath + '\\' + 'log')
    csh(savePath + '\\' + today)

    # 删除已解压过的文件
    def del_old_zip(file_path):
        os.remove(file_path)

    def unRar(file_path, root):
        # 开始
        # rarfile打开rar文件
        z = rarfile.RarFile(f'{file_path}', 'r')
        # 解压
        z.extractall(path=f"{root}")  # path为解压路径，解包后位于该路径下

    def start_dir_make(root, dirname):
        os.chdir(root)
        os.mkdir(dirname)
        return os.path.join(root, dirname)

    compSucces = open(savePath + '\\' + 'log' + '\\' + today + 'compSucces.txt', 'a+')
    print('-----------------' + today + now + '-----------------', file=compSucces)
    compFaile = open(savePath + '\\' + 'log' + '\\' + today + 'compFaile.txt', 'a+')
    print('-----------------' + today + now + '-----------------', file=compFaile)
    for root, dirs, files in os.walk(rar_path):
        for name in files:
            if name.endswith(file_flag):
                try:
                    # 创建文件夹
                    new_ws = start_dir_make(root, name.replace(file_flag, ''))
                    # zip文件地址
                    zip_path = os.path.join(root, name)
                    # 解压
                    unRar(zip_path, new_ws)
                    # desPath = savePath + '\\'+today+'\\' + name
                    desPath = savePath + '\\' + today + '\\'  + '\\' + name
                    csh(savePath + '\\' + today  )
                    shutil.copy(zip_path, desPath)
                    # 一定要备份或先测试，不然可能会凉，自己选择修改
                    del_old_zip(zip_path)
                    # # # 去掉多余的文件结构
                    # rem_dir_extra(root, name.replace(file_flag, ''))
                    print(f'{root}\\{name}'.join(['文件：[', ']解压完成\n']), file=compSucces)
                except Exception as e:
                    print(e, file=compFaile)
doCompRar()

    # for opt in rar_conf.options('rartype'):
    #     rarPath = parent_path + '\\' + opt
    #     rarType = rar_conf.get('rartype', opt)
    #     if rarType == '1':
    #         compSucces = open(savePath + '\\' + 'log' + '\\' + opt + today + 'compSucces.txt', 'a+')
    #         print('-----------------' + today + now + '-----------------', file=compSucces)
    #         compFaile = open(savePath + '\\' + 'log' + '\\' + opt + today + 'compFaile.txt', 'a+')
    #         print('-----------------' + today + now + '-----------------', file=compFaile)
    #         print(rarPath+'1', rarType+'2')
    #         for root, dirs, files in os.walk(rarPath):
    #             for name in files:
    #                 if name.endswith(file_flag):
    #                     try:
    #                         # 创建文件夹
    #                         # new_ws = start_dir_make(root, name.replace(file_flag, ''))
    #                         # zip文件地址
    #                         zip_path = os.path.join(root, name)
    #                         # 解压
    #                         # flag = decompress(zip_path, new_ws)
    #                         unRar(zip_path, root)
    #                         # desPath = savePath + '\\'+today+'\\' + name
    #                         desPath = savePath + '\\' + today + '\\' + opt + '\\' + name
    #                         csh(savePath + '\\' + today + '\\' + opt)
    #                         shutil.copy(zip_path, desPath)
    #                         # 一定要备份或先测试，不然可能会凉，自己选择修改
    #                         del_old_zip(zip_path)
    #                         # # # 去掉多余的文件结构
    #                         # rem_dir_extra(root, name.replace(file_flag, ''))
    #                         print(f'{root}\\{name}'.join(['文件：[', ']解压完成\n']), file=compSucces)
    #                     except Exception as e:
    #                         print(e, file=compFaile)
    #     elif rarType == '2':
    #         compSucces = open(savePath + '\\' + 'log' + '\\' + opt + today + 'compSucces.txt', 'a+')
    #         print('-----------------' + today + now + '-----------------', file=compSucces)
    #         compFaile = open(savePath + '\\' + 'log' + '\\' + opt + today + 'compFaile.txt', 'a+')
    #         print('-----------------' + today + now + '-----------------', file=compFaile)
    #         print(parent_path + '\\' + opt + '3' , rarType)
    #         for root, dirs, files in os.walk(rarPath):
    #             for name in files:
    #                 if name.endswith(file_flag):
    #                     try:
    #                         # 创建文件夹
    #                         new_ws = start_dir_make(root, name.replace(file_flag, ''))
    #                         # zip文件地址
    #                         zip_path = os.path.join(root, name)
    #                         # 解压
    #                         # flag = decompress(zip_path, new_ws)
    #                         unRar(zip_path, new_ws)
    #                         # desPath = savePath + '\\'+today+'\\' + name
    #                         desPath = savePath + '\\' + today + '\\' + opt + '\\' + name
    #                         csh(savePath + '\\' + today + '\\' + opt)
    #                         print(zip_path,'----',desPath)
    #                         shutil.copy(zip_path, desPath)
    #                         # 一定要备份或先测试，不然可能会凉，自己选择修改
    #                         del_old_zip(zip_path)
    #                         # # # 去掉多余的文件结构
    #                         # rem_dir_extra(root, name.replace(file_flag, ''))
    #                         print(f'{root}\\{name}'.join(['文件：[', ']解压完成\n']), file=compSucces)
    #                     except Exception as e:
    #                         print(e, file=compFaile)
    #     else:
    #         pass