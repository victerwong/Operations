import os
import glob
import time


def getFileAtt(folder_name, contains_name):
    print(folder_name)
    os.chdir(folder_name)
    file_names = os.listdir("./")
    file_att_list = []
    for name in file_names:
        print("是不是文件：", os.path.isfile(name))
        if os.path.isfile(name):
            name = os.path.abspath(name)
            # 返回一个元组，元组第二个元素是扩展名
            if os.path.splitext(name)[1] == ".zip":
                unzip = os.path.splitext(name)[0]
                order = '\"C:\\Program Files\\WinRAR\\WinRAR.exe\" x \"{0}\" -o' + folder_name + ' -r'
                print(order)
                cmd = order.format(name)
                os.popen(cmd)
                # 不设置延时会导致还没有解压完，就开始去找文件，导致找到文件错误
                time.sleep(1)
                path1 = glob.glob(unzip + '\**', recursive=True)
                # print (path1)
                file_att_list.append(path1)


            elif os.path.splitext(name)[1] == ".rar":
                unzip = os.path.splitext(name)[0]
                order = '\"C:\\Program Files\\WinRAR\\WinRAR.exe\" -x '+unzip+'.rar' +'-o ' + folder_name + ' -r'
                print(order)
                cmd = order.format(name)
                os.popen(cmd)
                time.sleep(1)
                path1 = glob.glob(unzip + '\**', recursive=True)
                # print (path1)
                file_att_list.append(path1)

            elif os.path.splitext(name)[1] == ".7z":
                unzip = os.path.splitext(name)[0]
                order = '\"C:\\Program Files\\WinRAR\\WinRAR.exe\" x \"{0}\" -o' + folder_name + ' -r'
                cmd = order.format(name)
                os.popen(cmd)
                time.sleep(1)
                path1 = glob.glob(unzip + '\**', recursive=True)
                # print (path1)
                file_att_list.append(path1)

            elif os.path.splitext(name)[1] == ".gzip":
                unzip = os.path.splitext(name)[0]
                order = '\"C:\\Program Files\\WinRAR\\WinRAR.exe\" x \"{0}\" -o' + folder_name + ' -r'
                cmd = order.format(name)
                os.popen(cmd)
                time.sleep(1)
                path1 = glob.glob(unzip + '\**', recursive=True)
                # print (path1)
                file_att_list.append(path1)

            elif os.path.splitext(name)[1] == ".tar":
                unzip = os.path.splitext(name)[0]
                order = '\"C:\\Program Files\\WinRAR\\WinRAR.exe\" x \"{0}\" -o' + folder_name + ' -r'
                cmd = order.format(name)
                os.popen(cmd)
                time.sleep(1)
                path1 = glob.glob(unzip + '\**', recursive=True)
                # print (path1)
                file_att_list.append(path1)

            elif os.path.splitext(name)[1] == ".bzip2":
                unzip = os.path.splitext(name)[0]
                order = '\"C:\\Program Files\\WinRAR\\WinRAR.exe\" x \"{0}\" -o' + folder_name + ' -r'
                cmd = order.format(name)
                os.popen(cmd)
                time.sleep(1)
                path1 = glob.glob(unzip + '\**', recursive=True)
                # print (path1)
                file_att_list.append(path1)
            else:
                # print(name)
                file_att_list.append(name)

    fileAtt = ''

    for att_list in file_att_list:
        if (contains_name in att_list):
            print("*********" + att_list)
            fileAtt = att_list
            break
        for att in att_list:
            if (contains_name in att):
                fileAtt = att
                break

    print('最后得到需要路径为：' + fileAtt)
    return fileAtt


getFileAtt(r'D:\Codes\unZip\Test\010300808785银河资本-国企增持1号资产管理计划', '.rar')