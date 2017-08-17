#!/usr/bin/env python
# _*_coding:utf-8 _*_
from django.shortcuts import render, HttpResponse
from Daily_app.views.account import login_sso
from IDC_app.manage import new_data_manage
from IDC_app.manage import asset_manage
import json


@login_sso
def add_new_data(request):
    # 添加新的数据
    ret = new_data_manage.create_new_data().__dict__
    return HttpResponse(json.dumps(ret))


@login_sso
def idc_list(request):
    # 展示  首页
    user_info = request.userinfo
    if request.method == "POST":
        data = request.POST.get("sn")
        print "dddddddddddddddddddddddd", data
        ret = asset_manage.get_search_asset(data).__dict__
        print "ret=====", ret
        return render(request, "idc/idc_show.html", {'userinfo': user_info, 'ret': ret})
    return render(request, "idc/idc_show.html", {'userinfo': user_info})


@login_sso
def check_data(request):
    # 搜索数据
    if request.method == "POST":
        input_data = request.POST.get('input_data')
        print "dddddddddddddddddddddddd", input_data
        return_dict = dict()
        return_dict['search_data'] = asset_manage.get_search_asset(input_data).__dict__        # 搜索的数据
        return_dict['pro_type'] = asset_manage.get_all_pro_type().__dict__        # 所有项目类型  用于前端创建select
        return HttpResponse(json.dumps(return_dict))
