
# from unrar import rarfile
# #
# # # def rar1(file_path):
# # # #     # 开始
# # # #     # rarfile打开rar文件
# # # #     z = rarfile.RarFile(file_path, 'r')
# # # #     # 解压
# # # #     try:
# # # #         z.extractall(path=file_path)  # 在当前位置直接解压
# # # #     except Exception as  e:
# # # #         print(e)
# # # # rar1(r'D:\Codes\unZip\temp\010300808785银河资本-国企增持1号资产管理计划\1126.rar')
# #
# # rf = rarfile.RarFile(r'D:\Codes\unZip\temp\010300808785银河资本-国企增持1号资产管理计划\1126.rar',mode='r')
# # rf.extractall(r'D:\Codes\unZip\temp\010300808785银河资本-国企增持1号资产管理计划\1126')

#流程总数：83
#部门、人员调整：
#入职：
#离职：
# import os,sys,time,shutil,configparser
#
#
# def readConf(file,section,option):
#     # cur_path = os.path.dirname(os.path.realpath(__file__))    #这里是获取当前路径的办法
#     abspath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 这里是获取当前路径的父路径
#     conf=configparser.ConfigParser()
#     conf.read(abspath + '\Conf'+'\\'+file, encoding='utf-8-sig')
#     print(abspath + '\Conf'+'\\'+file,)
#     parent_path = conf.get(section,option)
#     return parent_path
#
# def Conf(file):
#     abspath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 这里是获取当前路径的父路径
#     conf=configparser.ConfigParser()
#     conf.read(abspath + '\Conf'+'\\'+file, encoding='utf-8-sig')
#
#
# print()
# def confread():
#     cf = configparser.ConfigParser()
#     exeruningpath = os.path.dirname(sys.executable)
#     exepath = os.path.dirname(sys.path[0])
#     print(exeruningpath,exepath)
    # if os.path.exists(exepath + "\Editor_Excel\config.ini"):
    #     print(exepath + "\Editor_Excel\config.ini")
    #     cf.read(exepath + "\Editor_Excel\config.ini")
    # else:
    #     print(exepath + "\config.ini")
    #     cf.read(exeruningpath + "\config.ini")

from decompressFiles import doCompRar

doCompRar()


def conf(file):
    abspath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 这里是获取当前路径的父路径
    conf = configparser.ConfigParser()
    conf.read(abspath + '\Conf' + '\\' + file, encoding='utf-8-sig')
    return conf

parent_path = conf('svrcfg.ini').get('rarfile', 'parent_path')
savePath = conf('svrcfg.ini').get('rarfile', 'savePath')


for opt in conf('rarcfg.ini').options('rartype'):
    rarPath = parent_path + '\\' + opt
    rarType = conf('rarcfg.ini').get('rartype', opt)