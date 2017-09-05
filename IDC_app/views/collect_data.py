#!/usr/bin/env python
# _*_coding:utf-8 _*_
from django.shortcuts import render, HttpResponse
from Daily_app.views.account import login_sso
from IDC_app.manage import collect_manage
import json


@login_sso
def statistics(request):
    # 将统计数据返回前端
    if request.method == "POST":
        ret = collect_manage.collect_all_data().__dict__

        return HttpResponse(json.dumps(ret))
