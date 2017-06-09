#!/usr/bin/env python
# _*_coding:utf-8 _*_

from Daily_app.models import user_models


def get_dba_user():
    '''
    获取DBA的用户
    '''
    ret = user_models.UserInfo.objects.filter(user_type__caption="DBA")
    return ret


def get_sa_user():
    '''
    获取SA用户
    '''
    ret = user_models.UserInfo.objects.filter(user_type__caption="SA").filter(task_id__gt=0)
    return ret


def get_userinfo_by_username(username):
    '''
    根据sso返回的username来获取用户信息
    '''
    ret = user_models.UserInfo.objects.filter(username=username)
    return ret




