#!/usr/bin/env python
# _*_coding:utf-8 _*_

"""
处理ansible日志的视图
"""

from Daily_app.views.account import login_sso
from django.shortcuts import render, HttpResponse
from ansible_app.manage import cmd_manager
from ansible_app.manage import file_manager
from OM_platform import settings
import json


@login_sso
def ansible_log(request):
    '''
    ansible日志视图
    '''
    user_info = request.userinfo
    return render(request, 'log/ansible_log.html', {'userinfo': user_info})
