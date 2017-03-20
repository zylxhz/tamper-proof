# coding=utf-8
from django.db import models

# Create your models here.
class System(models.Model):
    name = models.CharField(u'系统', max_length=100)
    english_name = models.CharField(u'系统的英文名称', max_length=100)

class Node(models.Model):
    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    username = models.CharField(u'用户名', max_length=20)
    password = models.CharField(u'密码', max_length=20)
    system = models.CharField(u'系统名称', max_length=100)
    path = models.FilePathField(u'监视路径')

class FileMd5(models.Model):
    ip = models.GenericIPAddressField()
    path = models.FilePathField(u'文件路径')
    md5 = models.CharField(max_length=128)
