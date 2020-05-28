
import os,configparser

##获取指定目录下的子目录文件夹名称列表,并写入配置文件：
def writeConf(attPath,setion):
    config = configparser.ConfigParser()
    config.read('..//Conf/rarcfg.ini', encoding='utf-8-sig')
    try:
        for item in os.listdir(attPath):
            ##过滤目录下的文件，只筛选子目录
            newPath=attPath+'\\'+item
            if os.path.isdir(newPath) ==True:
                if item == 'Thumbs.db' or item =='':
                    pass
                else:
                    if config.has_section(setion) == False :
                        config.add_section(setion)
                    else:
                        pass
                dirOpt = config.options(setion)
                if item in dirOpt:
                    pass
                else:
                    config.set('rartype',item,'0')
                    with open('..//Conf/rarcfg.ini', 'w+',encoding='utf-8') as configfile:
                        config.write(configfile)
            else:
                pass
    except Exception as e:
        print(e)


# writeConf(r'D:\Codes\unZip','rartype')
