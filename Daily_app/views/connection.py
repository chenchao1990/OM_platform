#!/usr/bin/env python
# _*_coding:utf-8 _*_
from django.shortcuts import render, HttpResponse
from Daily_app.manage import connection_manager
from Daily_app.views.account import login_sso
from OM_platform import settings
import json
import os


@login_sso
def ping(request):
    '''
    ping
    '''
    user_info = request.userinfo

    return render(request, 'connection/ping.html', {'userinfo': user_info})


def single_ping(request):
    '''
    处理用户输入的精准IP地址
    '''
    if request.method == "POST":
        data = request.POST.get("ip_list")                 # 将用户输入的IP地址列表获取
        print "single---------------ping", data
        ret = connection_manager.single_ping(data).__dict__
        return HttpResponse(json.dumps(ret))


def rang_ping(request):
    '''
    处理用户输入的精准IP地址段
    '''
    if request.method == "POST":
        data = request.POST.get("ip_dict")                 # 将用户输入的IP地址列表获取
        print "rang_____________ip", data
        ret = connection_manager.rang_ping(data).__dict__
        return HttpResponse(json.dumps(ret))


def upload_ping_file(request):

    ping_dir = settings.PING_DIR
    print "FILE_______________DIR", ping_dir
    if request.method == "POST":
        inp_file = request.FILES          # 上传的文件会在request.FILES里
        file_obj = inp_file.get('f1')    # 根据前端设置的name属性值获取相对应的文件

        filename = file_obj.name              # 获取文件名
        ret = connection_manager.upload_ping_file(file_obj, filename, ping_dir).__dict__
        print "file_ping_________________", ret
        return HttpResponse(json.dumps(ret))


def file_ping(request):
    '''
    根据前端获取的文件名 读取文件内容 去ping
    '''
    if request.method == "POST":
        file_name = request.POST.get('file_name')
        file_dir = settings.PING_DIR
        ret = connection_manager.file_ping(file_name, file_dir).__dict__
        return HttpResponse(json.dumps(ret))


def get_ping_file(request):
    '''
    获取所有上传的ping文件
    '''
    if request.method == "POST":

        file_dir = settings.PING_DIR
        ret = connection_manager.get_ping_file(file_dir).__dict__
        print "retttttttttttttttttttttt", ret
        return HttpResponse(json.dumps(ret))


def delete_ping_file(request):
    '''
    获取所有上传的ping文件
    '''
    if request.method == "POST":
        data = request.POST.get("opt")
        if data == "delete":
            file_dir = settings.PING_DIR
            ret = connection_manager.delete_ping_file(file_dir).__dict__

            return HttpResponse(json.dumps(ret))
















