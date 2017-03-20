# coding=utf-8

import paramiko
import os

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
            self.logger.info(errinfo)
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

    def close(self):
        self.client.close()