# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileMd5',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.GenericIPAddressField()),
                ('path', models.CharField(max_length=256, verbose_name='\u6587\u4ef6\u8def\u5f84')),
                ('md5', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.GenericIPAddressField()),
                ('port', models.IntegerField()),
                ('username', models.CharField(max_length=20, verbose_name='\u7528\u6237\u540d')),
                ('password', models.CharField(max_length=20, verbose_name='\u5bc6\u7801')),
                ('system', models.CharField(max_length=100, verbose_name='\u7cfb\u7edf\u540d\u79f0')),
                ('root_path', models.CharField(max_length=256, verbose_name='\u76d1\u89c6\u7684\u6839\u8def\u5f84')),
                ('skip_paths', models.CharField(max_length=1024, verbose_name='\u65e0\u9700\u76d1\u63a7\u7684\u8def\u5f84')),
            ],
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u7cfb\u7edf')),
                ('english_name', models.CharField(max_length=100, verbose_name='\u7cfb\u7edf\u7684\u82f1\u6587\u540d\u79f0')),
            ],
        ),
    ]
