# coding=utf-8
from django.shortcuts import render_to_response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import get_template
from django.template import RequestContext
from django.template.context import Context
from django.views.decorators.csrf import csrf_exempt
from .forms import UserForm, NodeForm, PathForm
from .models import System
from django.contrib.auth.models import Group,User
from .sshproxy import SSHProxy
import logging
import os
import time
import paramiko
import json

#日志根目录
LOG_ROOT = 'C:\\testlog'

#当前时间
current = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))

if not os.path.exists(LOG_ROOT):
    os.makedirs(LOG_ROOT)

# 配置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=LOG_ROOT + os.path.sep + current + '.log',
                    filemode='w')

logger = logging.getLogger('Main')
cur_system = ''
system_info = {}

# Create your views here.

#显示所有有效用户的界面
def ui_user_info(request):
    t = get_template("user_info.html")
    users = User.objects.filter(is_active=True)
    context = {
        'users': users,
    }
    html = t.render(context)
    return HttpResponse(html)

#增加用户的界面
def ui_add_user(request):
    t = get_template('add_user.html')
    c = RequestContext(request)
    html = t.render(c)
    return HttpResponse(html)

#实际执行增加用户操作
@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            print 'form is valid'
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            role = data['role']
            user = User.objects.create_user(username, password)
            logger.info('create user' + username)
            group = Group.objects.get(name=role)
            user.groups=[group]
            user.save()
            return HttpResponseRedirect('/users/')
    else:
        form = UserForm()
    return render_to_response('add_user.html', {'form': form})

#删除选中的用户，即置用户状态为无效
@csrf_exempt
def delete_users(request):
    if request.method == 'POST':
        user_id_list = request.REQUEST.getlist('selected_user_id')
        for cur_id in user_id_list:
            user = User.objects.get(id=cur_id)
            print user.username
            user.is_active=False
            user.save()
    return HttpResponseRedirect('/users/')

def ui_add_task(request):
    t = get_template('add_task.html')
    c = RequestContext(request)
    html = t.render(c)
    return HttpResponse(html)

# 系统选择页面
def select_system(request):
    systems = System.objects.all()
    context = {'systems': systems}
    t = get_template('select_system.html')
    html = t.render(context)
    return HttpResponse(html)

#显示增加节点页面
def add_node(request):
    logger.info(u'增加节点')
    try:
        cur_system = request.GET.get('system')
        request.session['system'] = cur_system
        cur_system = request.session.get('system')
    except:
        cur_system = request.session.get('system')
    logger.info(u'选择的系统是:' + cur_system)
    request.session['node_list'] = []
    t = get_template('add_node.html')
    c = RequestContext(request)
    html = t.render(c)
    return HttpResponse(html)

#处理用户增加监控节点的请求
@csrf_exempt
def process_add_node(request):

    return HttpResponseRedirect('/selectroot/')


#显示监控根目录选择界面
def select_root(request):
    logger.info(u'显示监控根目录选择界面')
    if request.method == 'POST':
        form = NodeForm(request.POST)
        if form.is_valid():
            logger.info('NodeForm is valid')
            data = form.cleaned_data
            ip = data['ip']
            port = data['port']
            username = data['username']
            password = data['password']
            logger.info('ip: ' + ip + ' , port: ' + port +  ' , username: ' + username + ' , password: ' + password)
            request.session['node'] = data
    t = get_template('select_root.html')
    html = t.render(Context())
    return HttpResponse(html)

#获得下一级的目录信息
def get_sub(request):
    logger.info(u'准备获得下一级的目录信息')
    path = request.GET.get('path')
    logger.info('path: ' + path)
    proxy = SSHProxy(logger)
    node = request.session['node']
    ip = node['ip']
    port = node['port']
    username = node['username']
    password = node['password']
    logger.info('ip: ' + ip + ' , port: ' + port +  ' , username: ' + username + ' , password: ' + password)
    proxy.connect(ip, port, username, password)
    dir_name = os.path.basename(path)
    if dir_name == '':
        dir_name = '/'
    data = {'title' : dir_name, 'folder' : True, 'expanded' : True}
    proxy.get_sub(path, data)
    logger.info(data)
    return HttpResponse(json.dumps(data), content_type='application/json')

#设置根目录
def set_root(request):
    logger.info(u'设置根目录')
    path = request.GET.get('path')
    node = request.session['node']
    node['root'] = path
    request.session['node'] = node
    return HttpResponseRedirect('/selectskipdirs/')

#选择无需监控的目录
def select_skip_dirs(request):
    logger.info(u'选择无需监控的目录')
    node = request.session['node']
    root_dir = node['root']
    context = {'root_dir' : root_dir}
    print root_dir
    t = get_template('select_skip_dirs.html')
    html = t.render(context)
    return HttpResponse(html)

