#!/usr/bin/env python
# _*_coding:utf-8 _*_
from django.shortcuts import render, HttpResponse
from Daily_app.views.account import login_sso
from Daily_app.manage import password_manage
from OM_platform import settings
import json


@login_sso
def password_check(request):
    '''
    密码查询页面
    '''
    user_info = request.userinfo
    if request.method == "POST":
        data = request.POST
        ret = password_manage.password_check(data).__dict__
        return HttpResponse(json.dumps(ret))

    return render(request, 'pwd_manage/password_check.html', {'userinfo': user_info})
    # return render(request, 'pwd_manage/password_check.html')


@login_sso
def upload_password_file(request):
    pwd_dir = settings.PASSWORD_DIR                    # 导入接受密码文件目录
    if request.method == "POST":
        inp_file = request.FILES            # 上传的文件会在request.FILES里
        file_obj = inp_file.get('pwd')       # 根据前端设置的name属性值获取相对应的文件

        filename = file_obj.name              # 获取文件名
        ret = password_manage.upload_pwd_file(file_obj, filename, pwd_dir).__dict__
        return HttpResponse(json.dumps(ret))


@login_sso
def get_password_file(request):
    '''
    获取所有上传的ping文件
    '''
    if request.method == "POST":

        pwd_dir = settings.PASSWORD_DIR
        ret = password_manage.get_pwd_file(pwd_dir).__dict__
        return HttpResponse(json.dumps(ret))


@login_sso
def delete_password_file(request):
    '''
    删除所有密码文件
    '''
    if request.method == "POST":
        data = request.POST.get("opt")
        if data == "delete":
            file_dir = settings.PASSWORD_DIR
            ret = password_manage.delete_pwd_file(file_dir).__dict__

            return HttpResponse(json.dumps(ret))


@login_sso
def run_check_file(request):
    '''
    根据前端获取的文件名 读取文件内容 去检查密码
    '''
    if request.method == "POST":

        data = request.POST
        file_dir = settings.PASSWORD_DIR
        ret = password_manage.file_check_pwd(data, file_dir).__dict__
        return HttpResponse(json.dumps(ret))


@login_sso
def password_import(request):
    '''
    密码导入
    '''
    user_info = request.userinfo
    username = user_info.get('cn_name', '1')
    if request.method == "POST":
        data = request.POST
        file_dir = settings.PASSWORD_DIR
        ret = password_manage.file_import_pwd(data, file_dir, username).__dict__
        return HttpResponse(json.dumps(ret))

    return render(request, 'pwd_manage/password_import.html', {'userinfo': user_info})


@login_sso
def password_init(request):
    '''
    修改服务器密码 并保存
    '''
    user_info = request.userinfo
    username = user_info.get('cn_name', '1')
    if request.method == "POST":
        data = request.POST
        file_dir = settings.PASSWORD_DIR
        ret = password_manage.change_pwd_and_save(data, file_dir, username).__dict__
        return HttpResponse(json.dumps(ret))

    return render(request, 'pwd_manage/password_init.html', {'userinfo': user_info})


def password_queue_data(request):
    '''
    从redis队列里获取数据
    '''
    if request.method == "POST":
        data = request.POST
        print "pppppppppppppppppost_data", data
        ret = password_manage.get_data_from_redis(data).__dict__
        return HttpResponse(json.dumps(ret))


@login_sso
def password_server(request):
    '''
    密码初始化
    '''
    user_info = request.userinfo
    username = user_info.get('cn_name', '1')
    if request.method == "POST":
        data = request.POST
        file_dir = settings.PASSWORD_SERVER
        ret = password_manage.change_manager_pwd(data, file_dir, username).__dict__
        return HttpResponse(json.dumps(ret))
    return render(request, 'pwd_manage/password_server.html', {'userinfo': user_info})


@login_sso
def upload_password_server(request):
    '''
    上传修改管理口密码的文件
    '''
    pwd_dir = settings.PASSWORD_SERVER                    # 导入接受密码文件目录
    print "server_______________DIR", pwd_dir
    if request.method == "POST":
        inp_file = request.FILES            # 上传的文件会在request.FILES里
        file_obj = inp_file.get('server')       # 根据前端设置的name属性值获取相对应的文件

        filename = file_obj.name              # 获取文件名
        ret = password_manage.upload_pwd_file(file_obj, filename, pwd_dir).__dict__
        return HttpResponse(json.dumps(ret))


@login_sso
def get_server_file(request):
    '''
    获取所有上传的管理口文件
    '''
    if request.method == "POST":
        print "8888888888888888888888888888888888"
        server_dir = settings.PASSWORD_SERVER
        ret = password_manage.get_server_file(server_dir).__dict__
        return HttpResponse(json.dumps(ret))


@login_sso
def delete_server_file(request):
    '''
    删除指定的管理口文件
    '''
    if request.method == "POST":
        data = request.POST.get("opt")
        if data == "delete":
            server_dir = settings.PASSWORD_SERVER
            ret = password_manage.delete_pwd_file(server_dir).__dict__

            return HttpResponse(json.dumps(ret))


@login_sso
def change_server_pwd(request):
    '''
    获取文件名 执行修改BMC的管理密码
    '''
    user_info = request.userinfo
    username = user_info.get('cn_name', '1')
    if request.method == "POST":
        data = request.POST
        file_dir = settings.PASSWORD_SERVER
        ret = password_manage.change_server_password(data, file_dir, username).__dict__
        return HttpResponse(json.dumps(ret))















