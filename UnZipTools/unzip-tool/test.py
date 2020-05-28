import os,time,shutil,zipfile
from unrar import rarfile

# 首先引入需要的工具包
# shutil为后期移动文件所需

# 定义相关路径：
parent_path = r'D:\unZip\Test\010300808785银河资本-国企增持1号资产管理计划'
savePath=r'D:\unZip\Test\unZip'

# 文件类型选择
file_flag = '.rar'
today = time.strftime('%y%m%d')
now = time.strftime('%H%M%S')

##初始化目录：
def csh(dir):
    if os.path.exists(dir) == True and os.path.isdir(dir) == True:
        pass
    else:
        os.mkdir(dir)

# 删除已解压过的文件
def del_old_zip(file_path):
    os.remove(file_path)

# 解压
def zip_decompress(file_path, root):
    # 开始
    # zipfile打开zip文件
    z = zipfile.ZipFile(f'{file_path}', 'r')
    # 解压
    z.extractall(path=f"{root}")  # path为解压路径，解包后位于该路径下
    # 判断是否需要重复解包
    for names in z.namelist():
        if names.endswith(file_flag):
            z.close()
            return 1
    # 结束
    z.close()
    return 0


def rar_decompress(file_path, root):
    # 开始
    # rarfile打开rar文件
    z = rarfile.RarFile(f'{file_path}', 'r')
    # 解压
    z.extractall(path=f"{root}")  # path为解压路径，解包后位于该路径下
    # 判断是否需要重复解包
    for names in z.namelist():
        if names.endswith(file_flag):
            z.close()
            return 1
    # 结束
    z.close()
    return 0

csh(savePath)
csh(savePath+ '\\' + 'log')
csh(savePath + '\\' + today)

decompress = None
if file_flag == '.zip':
    decompress = zip_decompress
elif file_flag == '.rar':
    decompress = rar_decompress
else:
    pass

def start_dir_make(root, dirname):
    os.chdir(root)
    os.mkdir(dirname)
    return os.path.join(root, dirname)

def decomp(parent_path):
    #  循环遍历文件夹
    for root, dirs, files in os.walk(parent_path):
        # 读取文件名
        for name in files:
            if name.endswith(file_flag):
                try:
                    # 创建文件夹
                    new_ws = start_dir_make(root, name.replace(file_flag, ''))
                    # zip文件地址
                    zip_path = os.path.join(root, name)
                    # 解压
                    # flag = decompress(zip_path, new_ws)
                    decompress(zip_path, new_ws)
                    # desPath = savePath + '\\'+today+'\\' + name
                    desPath = savePath + '\\' + today+'\\'+ name
                    shutil.copy(zip_path, desPath)
                    # 一定要备份或先测试，不然可能会凉，自己选择修改
                    del_old_zip(zip_path)
                    # # # 去掉多余的文件结构
                    # rem_dir_extra(root, name.replace(file_flag, ''))
                    compSucces = open(savePath+ '\\' + 'log'+'\\' + today+'compSucces.txt', 'a+')
                    print('-----------------' + today + now + '-----------------',file=compSucces)
                    print(f'{root}\\{name}'.join(['文件：[', ']解压完成\n']),file=compSucces)
                except Exception as e:
                    compFaile = open(savePath+ '\\' + 'log'+'\\' + today + 'compFaile.txt', 'a+')
                    print('-----------------'+today+now+'-----------------',file=compFaile)
                    print(e,file=compFaile)

decomp(parent_path)