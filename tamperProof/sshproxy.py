# coding=utf-8

import paramiko
from .models import FileMd5

class SSHProxy:
    def __init__(self, logger):
        self.logger = logger
        self.client = paramiko.SSHClient()  # 绑定实例
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


    #获得path路径下的文件信息，并存储在data['children']中
    def get_sub(self, path, data):
        self.logger.info('path : ' + path)
        children = []
        stdin, stdout, stderr = self.client.exec_command('ls ' + path)
        for line in stdout.readlines():
            file_name = line.strip('\n')
            self.logger.info(file_name)
            abs_path = path + '/' + file_name
            stdin, stdout, stderr = self.client.exec_command('cd ' + abs_path)
            errinfo = stderr.readlines()
            #不是目录，cd命令会有报错
            if errinfo:
                child_data = {'folder' : False}
            else:
                child_data = {'folder' : True}
            child_data['title'] = file_name
            children.append(child_data)
        data['children'] = children




    def connect(self, ip, port, username, password):
        self.logger.info(u'开始SSH连接')
        result = False
        try:
            self.client.connect(ip, int(port), username, password, timeout=15)
            self.logger.info(u'SSH连接成功')
            result = True
        except Exception, e:
            self.logger.error(e.message)
            self.logger.info(u'SSH连接失败')
        return result

    def set_root(self):
        self.logger.info(u'设置监控的根目录')


    def prepare_monitor(self, ip, cur_path, skip_dirs):
        if cur_path in skip_dirs:
            self.logger.info(u'跳过 ' + cur_path)
            return
        stdin, stdout, stderr = self.client.exec_command('cd ' + cur_path)
        errinfo = stderr.readlines()
        #不是目录，cd命令会有报错
        if errinfo:
            stdin, stdout, stderr = self.client.exec_command("md5sum " + cur_path + " | awk  '{print $1}'")
            md5 = stdout.readline()
            print md5
            self.logger.info(cur_path + ' md5 is ' + md5)
            filemd5_instance = FileMd5(ip=ip, path=cur_path, md5=md5)
            filemd5_instance.save()
        #是目录
        else:
            stdin, stdout, stderr = self.client.exec_command('ls ' + cur_path)
            lines =  stdout.readlines()
            md5 = str(len(lines))
            self.logger.info(cur_path + ' md5 is ' + md5)
            filemd5_instance = FileMd5(ip=ip, path=cur_path, md5=md5)
            filemd5_instance.save()
            for line in lines:
                file_name = line.strip('\n')
                print file_name
                sub_path = cur_path + '/' + file_name
                self.prepare_monitor(ip,sub_path, skip_dirs)


    def close(self):
        self.client.close()