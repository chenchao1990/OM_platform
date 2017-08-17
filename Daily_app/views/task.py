#!/usr/bin/env python
# _*_coding:utf-8 _*_
from django.shortcuts import render, HttpResponse, redirect
from Daily_app.manage import task_manager
from Daily_app.manage import cloud_host_manager
from Daily_app.views.account import login_sso
import json
import datetime


def create_task_data(request):
    cur = datetime.datetime.now().year
    task_manager.create_task_data(cur)
    return HttpResponse(str(cur) + " task data is create successful!!!!")


# @login_auth
def task_show(request):

    return render(request, 'data_show/task_show.html')


# @login_auth
def task_show_all(request):

    ret = task_manager.get_task(2).__dict__
    return HttpResponse(json.dumps(ret))


# @login_auth
def task_show_month(request):
    s = datetime.datetime.now()
    if request.method == "POST":
        month_num = request.POST.get('month_id')
        if month_num:                               # 如果有月份 说明是在切换月份

            ret = task_manager.get_task(int(month_num)).__dict__
        else:                                       # 如果没有 说明是刚打开页面，自动跳转的当前月
            current_day = datetime.datetime.now().day
            ret = task_manager.get_task(s.month, current_day).__dict__
        return HttpResponse(json.dumps(ret))


@login_sso
def cloud_host(request):
    '''
    展示公司云主机数据
    '''
    user_info = request.userinfo
    ret = cloud_host_manager.get_all_company().__dict__
    if request.method == "POST":
        data = request.POST
        cloud_host_manager.add_new_cloud_data(data)
    return render(request, 'data_show/cloud_host.html', {'userinfo': user_info, 'all_company': ret})


@login_sso
def get_host_data(request):
    '''
    将云主机数量获取 展示到前端
    '''
    if request.method == "POST":
        ret = cloud_host_manager.get_all_host_data().__dict__
        return HttpResponse(json.dumps(ret))

#
# @login_sso
# def add_new_data(request):
#     '''
#     将云主机数量获取 展示到前端
#     '''
#     if request.method == "POST":
#         data = request.POST
#         print "dddddddddddddddddddd", data
#     return render(request)


@login_sso
def add_new_company(request):
    '''
    将云主机数量获取 展示到前端
    '''
    if request.method == "POST":
        data = request.POST
        print "dddddddddddddddddddd", data
        cloud_host_manager.add_new_company(data)
    return redirect('/cloud/')


@login_sso
def delete_day_data(request):
    '''
    将云主机数量获取 展示到前端
    '''
    if request.method == "POST":
        data = request.POST
        print "dddddddddddddddddddd", data
        ret = cloud_host_manager.delete_day_data(data).__dict__
    return HttpResponse(json.dumps(ret))

