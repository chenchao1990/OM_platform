#!/usr/bin/env python
# _*_coding:utf-8 _*_

from Daily_app.models import user_models
from overall.response.base_response import BaseResponse


def check_valid(**kwargs):
    response = BaseResponse()
    try:
        result = user_models.AdminInfo.objects.get(**kwargs)
        response.status = True
        response.data = result
    except Exception, e:
        response.message = str(e)
    return response


def get_userinfo(username):
    '''
    根据SSO返回的username  来获取本地库中用户的信息 没有则说明没有权限
    '''
    user_dict = {}
    ret = user_models.UserInfo.objects.filter(username=username)

    if len(ret) == 0:
        return False
    userinfo = ret[0]
    user_dict['cn_name'] = userinfo.cn_name
    user_dict['user_auth'] = userinfo.user_auth
    user_dict['group_auth_num'] = userinfo.user_type.code
    user_dict['user_id'] = userinfo.id

    return user_dict














