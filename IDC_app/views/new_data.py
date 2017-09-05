#!/usr/bin/env python
# _*_coding:utf-8 _*_
from django.shortcuts import render, HttpResponse
from Daily_app.views.account import login_sso
from IDC_app.manage import new_data_manage
from IDC_app.manage import asset_manage
from OM_platform import settings
import json


@login_sso
def add_new_data(request):
    # 添加新的数据
    idc_file_path = settings.IDC_FILES
    if request.method == "POST":
        inp_file = request.FILES
        file_obj = inp_file.get('idc-file')       # 根据前端设置的name属性值获取相对应的文件
        filename = file_obj.name              # 获取文件名
        ret = new_data_manage.create_new_data(file_obj, idc_file_path, filename).__dict__
        return HttpResponse(json.dumps(ret))


@login_sso
def idc_list(request):
    # 展示  首页
    user_info = request.userinfo
    if request.method == "POST":
        data = request.POST.get("sn")
        ret = asset_manage.get_search_asset(data).__dict__
        return render(request, "idc/idc_show.html", {'userinfo': user_info, 'ret': ret})
    return render(request, "idc/idc_show.html", {'userinfo': user_info})


@login_sso
def check_data(request):
    # 搜索数据
    if request.method == "POST":
        input_data = request.POST.get('input_data')
        return_dict = dict()
        return_dict['search_data'] = asset_manage.get_search_asset(input_data).__dict__        # 搜索的数据
        return_dict['pro_type'] = asset_manage.get_all_pro_type().__dict__        # 所有项目类型  用于前端创建select
        return HttpResponse(json.dumps(return_dict))


@login_sso
def update_data(request):
    # 更新数据
    if request.method == "POST":
        change_data = request.POST.get('data', None)       # 获取更新数据  一个列表
        ret = asset_manage.update_date(change_data).__dict__
        return HttpResponse(json.dumps(ret))


@login_sso
def statistics(request):
    # 数据统计
    if request.method == "POST":
        change_data = request.POST.get('data', None)       # 获取更新数据  一个列表
        ret = asset_manage.update_date(change_data).__dict__
        return HttpResponse(json.dumps(ret))


@login_sso
def new_idc_data(request):
    # 上传文件表格，添加新数据
    if request.method == "POST":
        change_data = request.POST.get('data', None)       # 获取更新数据  一个列表
        ret = asset_manage.update_date(change_data).__dict__
        return HttpResponse(json.dumps(ret))
