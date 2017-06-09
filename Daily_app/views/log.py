#!/usr/bin/env python
# _*_coding:utf-8 _*_
from django.shortcuts import render, HttpResponse
from Daily_app.manage import iptables_manage
from Daily_app.manage import log_manager
from overall.page import pager
from Daily_app.views.account import login_sso
from OM_platform.settings import now_time
import json


@login_sso
def iptables_log(request):
    user_info = request.userinfo
    return render(request, 'log/iptables_log.html', {'userinfo': user_info})


@login_sso
def iptables_log_show(request):
    '''
    获取日志信息 返回前端
    '''
    page = request.POST.get('page', None)
    all_count = iptables_manage.get_log_count()
    page_info = pager.PageInfo(page, all_count.data)

    ret = dict()
    ret['asset'] = iptables_manage.get_log_lists(page_info.start, page_info.end).__dict__
    ret['page'] = page_info.pager()
    ret['start'] = page_info.start
    result = json.dumps(ret)

    return HttpResponse(result)


@login_sso
def password_log(request):
    user_info = request.userinfo
    return render(request, 'log/password_log.html', {'userinfo': user_info})


@login_sso
def password_log_show(request):
    '''
    获取密码导入日志信息 返回前端
    '''
    page = request.POST.get('page', None)
    all_count = log_manager.get_pass_log_count()
    page_info = pager.PageInfo(page, all_count.data)

    ret = dict()
    ret['asset'] = log_manager.pass_log_data_list(page_info.start, page_info.end).__dict__
    ret['page'] = page_info.pager()
    ret['start'] = page_info.start
    result = json.dumps(ret)

    return HttpResponse(result)





















