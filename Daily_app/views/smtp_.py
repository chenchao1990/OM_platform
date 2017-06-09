#!/usr/bin/env python
# _*_coding:utf-8 _*_

from django.shortcuts import render, HttpResponse
from Daily_app.views.account import login_sso
from Daily_app.manage import smtp_manager
from OM_platform import settings
import json


@login_sso
def smtp_(request):
    '''
    添加smtp 配置 页面
    '''
    user_info = request.userinfo
    return render(request, 'connection/smtp.html', {'userinfo': user_info})


def smtp_add(request):
    '''
    接受页面发送的IP地址 添加到配置文件中
    '''
    if request.method == "POST":
        data = request.POST.get('ip_list')
        print "post_data", data, type(data)
        ret = smtp_manager.smtp_add(data).__dict__
        return HttpResponse(json.dumps(ret))























