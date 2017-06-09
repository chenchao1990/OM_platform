#!/usr/bin/env python
# -*- coding:utf-8 -*-
from OM_platform import settings
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
import json


# ########## 用于验证用户是否登陆的装饰器 ##########
def login_auth(func):
    """ 如果用户已经登陆，则执行相应的Views中的函数，否则，跳转至 settings中设置的LOGIN_URL地址，即：  '/account/login/'"""

    def wrapper(request, *args, **kwargs):
        result = request.session.get('auth_user', None)
        if not result:
            login_url = '%s?back=%s' % (settings.LOGIN_URL, request.path)
            return redirect(login_url)
        result = json.loads(result)
        request.username = result['name']
        request.user_id = result['id']
        request.weight = result['weight']
        response = func(request, *args, **kwargs)
        return response
    return wrapper
