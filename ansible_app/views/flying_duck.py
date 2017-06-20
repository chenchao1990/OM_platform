#!/usr/bin/env python
# _*_coding:utf-8 _*_

"""
处理ansible任务的地方
"""

from Daily_app.views.account import login_sso
from django.shortcuts import render, HttpResponse
from ansible_app.manage import cmd_manager
from ansible_app.manage import file_manager
from OM_platform import settings
import json


@login_sso
def cmd_view(request):
    '''
    处理命令的方法
    '''
    user_info = request.userinfo

    return render(request, 'ansible/cmd_run.html', {'userinfo': user_info})
    # return render(request, 'ansible/cmd_run.html')


@login_sso
def cmd_execute(request):
    '''
    接收前端传送 执行命令的各种参数 并检测执行
    '''

    if request.method == "POST":
        username = request.userinfo.get('cn_name', 'none')
        data = request.POST
        ret = cmd_manager.cmd_execute(data, username).__dict__
        return HttpResponse(json.dumps(ret))


@login_sso
def file_view(request):
    '''
    获取目录下上传的所有文件
    '''
    user_info = request.userinfo
    pwd_dir = settings.PASSWORD_DIR                    # 导入接受密码文件目录
    return render(request, 'ansible/upload_file.html', {'userinfo': user_info})


@login_sso
def upload_ip_file(request):
    '''
    上传IP文件
    :param request:
    :return:
    '''
    ipfile_dir = settings.IP_FILE_DIR                    # 导入接受IP文件目录
    if request.method == "POST":
        ip_file = request.FILES                 # 上传的文件会在request.FILES里
        file_obj = ip_file.get('ip-file')       # 根据前端设置的name属性值获取相对应的文件
        filename = file_obj.name                 # 获取文件名
        ret = file_manager.upload_ip_file(file_obj, filename, ipfile_dir).__dict__
        return HttpResponse(json.dumps(ret))


@login_sso
def upload_file(request):
    file_dir = settings.ANSIBLE_FILE_DIR                    # 导入接受IP文件目录
    if request.method == "POST":
        ip_file = request.FILES                         # 上传的文件会在request.FILES里
        file_obj = ip_file.get('upload_filename')       # 根据前端设置的name属性值获取相对应的文件
        # filename = file_obj.name                        # 获取文件名
        ret = file_manager.upload_file(file_obj, file_dir).__dict__
        return HttpResponse(json.dumps(ret))


@login_sso
def upload_script(request):
    script_dir = settings.SCRIPT_FILE_DIR                    # 导入接受IP文件目录
    if request.method == "POST":
        ip_file = request.FILES                         # 上传的文件会在request.FILES里
        file_obj = ip_file.get('upload_filename')       # 根据前端设置的name属性值获取相对应的文件
        # filename = file_obj.name                        # 获取文件名
        ret = file_manager.upload_file(file_obj, script_dir).__dict__
        return HttpResponse(json.dumps(ret))


@login_sso
def get_all_files(request):
    '''
    获取所有上传的ping文件
    '''
    if request.method == "POST":

        file_dir = settings.ANSIBLE_FILE_DIR
        ret = file_manager.get_upload_files(file_dir).__dict__
        return HttpResponse(json.dumps(ret))


@login_sso
def dispense_file(request):
    '''
    将前端选择的文件分发至服务器
    '''
    if request.method == "POST":
        username = request.userinfo.get('cn_name', 'none')
        ip_file_dir = settings.IP_FILE_DIR
        data = request.POST
        ret = file_manager.send_file(ip_file_dir, data, username).__dict__
        return HttpResponse(json.dumps(ret))


@login_sso
def run_script(request):
    '''
    执行脚本
    '''
    if request.method == "POST":
        username = request.userinfo.get('cn_name', 'none')
        script_dir = settings.SCRIPT_FILE_DIR
        host_dir = settings.IP_FILE_DIR
        data = request.POST
        print "ansible  script data", data
        ret = file_manager.run_script(script_dir, host_dir, data, username).__dict__
        return HttpResponse(json.dumps(ret))


@login_sso
def delete_file(request):
    '''
    删除目录中上传的文件
    '''
    if request.method == "POST":
        filename = request.POST.get('filename')
        file_type = request.POST.get('file_type')
        file_dir = None
        if file_type == 'script':
            file_dir = settings.SCRIPT_FILE_DIR
        elif file_type == 'file':

            file_dir = settings.ANSIBLE_FILE_DIR
        ret = file_manager.delete_upload_file(filename, file_dir).__dict__
        return HttpResponse(json.dumps(ret))


@login_sso
def execute_script(request):
    '''
    执行脚本的页面
    '''
    user_info = request.userinfo
    return render(request, 'ansible/run_script.html', {'userinfo': user_info})


@login_sso
def get_all_scripts(request):
    '''
    获取所有上传的脚本
    '''
    if request.method == "POST":

        script_dir = settings.SCRIPT_FILE_DIR
        ret = file_manager.get_upload_files(script_dir).__dict__
        return HttpResponse(json.dumps(ret))


