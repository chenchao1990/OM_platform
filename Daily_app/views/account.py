#!/usr/bin/env python
# _*_coding:utf-8 _*_

from django.shortcuts import render, HttpResponse, redirect
from Daily_app.form import user_form
from Daily_app.manage import account_manager
from Daily_app.model_handle import user_handle
import json


from django.conf import settings
from django.views.generic import TemplateView
import pytz
import requests
import datetime
from django.http import HttpResponseRedirect


def now(n=0):
    '''
    获取当前时区的时间
    :param n:
    :return:
    '''
    tz = pytz.timezone('Asia/Shanghai')     # 设置时区
    dt = datetime.datetime.now(tz)
    dt = dt + datetime.timedelta( days = n )
    return str(dt.strftime('%Y-%m-%d %H:%M:%S'))


class PublicView(TemplateView):
    userinfo = None
    template_name = 'error.html'

    def dispatch(self, request, *args, **kwargs):
        #login_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        login_time = now()                              # 获取当前时区的时间
        sign = request.REQUEST.get('sign', '')          # 获取请求中的 sign 值
        if sign != '':                                  # 如果sign不为空
            url = request.path                          # 跳转到sso.html  并携带sign值和 下一跳的URL
            return HttpResponseRedirect("/sso.html?token=%s&redirect_url=%s" % (sign, url))
        ssoUserInfo = None
        username = auth_sso(request)                            # 将请求的数据交给SSO的认证 发送post请求
        if not username:                                        # 如果sso请求返回的username为false
            url = request.get_full_path()                       # 获取请求的URL
            ssoUrl = "/sso.html?redirect_url=%s" % url          # 拼接跳转的URL
            return HttpResponseRedirect(ssoUrl)
        # userinfo = get_userinfo_by_username(username)           # 根据sso返回的username去获取本地数据库中的用户信息 字典
        # if not userinfo:                                    # 如果本地数据库中没有这个用户信息
        #     return HttpResponse("没有权限，请联系管理员高阳开通 gaoyang@gome.com.cn")
        '''
        处理登陆用户的cookie
        '''
        # if OperationLog.objects.filter(user_name=username, operation='login'):      # 如果本地数据库中有此用户登陆的信息
        #     login_cookie = str(OperationLog.objects.filter(user_name=username,operation='login').order_by('-operation_time')[0].login_cookie)       # 获取这个用户登陆的cookie
        #     if login_cookie != request.COOKIES['gome_sso_token']:       # 如果从本地库中获取的cookie不等于请求中的cookie  则新创建一条用户登陆的cookie
        #         OperationLog.objects.create(user_name=username,operation='login',type='login',operation_time=login_time,login_cookie=request.COOKIES['gome_sso_token'])
        # else:
        #     OperationLog.objects.create(user_name=username,operation='login',type='login',operation_time=login_time,login_cookie=request.COOKIES['gome_sso_token'])
        # self.userinfo = userinfo                    # 将用户的信息设置为动态字段
        self.username = username
        return super(PublicView, self).dispatch(request, *args, **kwargs)


# ########## 用于验证用户是否登陆的装饰器 ##########
def login_sso(func):
    """ 如果用户已经登陆，则执行相应的Views中的函数，否则，跳转至 settings中设置的LOGIN_URL地址，即：  '/account/login/'"""

    def wrapper(request, *args, **kwargs):
        sign = request.GET.get('sign', '')
        # sign = request.REQUEST.get('sign', '')          # 获取请求中的 sign 值
        if sign != '':
            url = request.path
            return HttpResponseRedirect("/sso.html?token=%s&redirect_url=%s" % (sign, url))
        username = auth_sso(request)
        if not username:
            url = request.get_full_path()
            ssoUrl = "/sso.html?redirect_url=%s" % url
            return HttpResponseRedirect(ssoUrl)

        userinfo = account_manager.get_userinfo(username)
        if not userinfo:
            return HttpResponse("没有权限，请联系管理员开通！！！")
        request.userinfo = userinfo
        # request.user_auth = userinfo['user_auth']
        # request.group_auth_num = userinfo['group_auth_num']
        response = func(request, *args, **kwargs)
        return response
    return wrapper


def logout_sso(request):

    domain_name = settings.CMDB_HOST            # 获取自己平台的域名
    domain_ip = settings.SSO_DOMAIN
    app_key = settings.APP_KEY

    # s = "http://10.126.59.18:8080/app/logout?redirectUrl=http://gom.ds.gome.com.cn/&appKey=7b37ca05cb0a4e759fdfc28bdb6ab31b"
    return HttpResponseRedirect("http://%s/app/logout?redirectUrl=http://%s&appKey=%s" % (domain_ip, domain_name, app_key))
    # return HttpResponseRedirect(s)


# sso登录
def auth_sso(request):
    '''
    将request中的请求数据提取出来， 向SSO发送认证的请求
    :param request:
    :return:
    '''
    if settings.SSO_TOKEN in request.COOKIES:           # 判断预设的TOKEN gome_sso_token 是否在请求的cookie中
        token = request.COOKIES.get(settings.SSO_TOKEN)             # 取出key为预设TOKEN的值
        url = "http://%s/app/token" % (settings.SSO_DOMAIN)         # 拼接URL  http://10.126.59.18:8080/app/token
        appkey = settings.APP_KEY                                   # APP_KEY = 337fe96ef8d0400c92cb71a85f1f1803
        headers = {'content-type': 'application/json', 'appKey': appkey}
        payload = {'token': token}
        respJson = requests.post(url, data=json.dumps(payload), headers=headers).json()  # 携带者URL token 和appkey发送post请求
        if respJson['code'] != 0:           # post请求返回的数据中  code的值不为0 说明请求错误 返回False
            return False
        else:                               # 否则没问题， 进一步处理post返回的数据
            # ret_dict = {}
            # ret_dict['user_id'] = respJson['data']['userId']                # 用户的id
            # ret_dict['username'] = respJson['data']['userName']             # 用户名
            # ret_dict['department'] = ""                                      # 环境
            # ret_dict['mobile'] = ""                                          # 电话
            # ret_dict['title'] = ""                                           # 标题
            # ret_dict['chinese_name'] = respJson['data']['userName']         # 中文名
            # user_dict = ret_dict
            username = respJson['data']['userName']
            return username                                                 # 返回用户名
    else:
        return False


# sso登录
class SSOView(TemplateView):
    template_name = 'auth/relay_sso.html'

    def get_context_data(self, **kwargs):
        context = super(SSOView, self).get_context_data(**kwargs)
        context['ssoDomain'] = settings.SSO_DOMAIN
        return context


def login(request):
    '''
    老的登陆方法  已弃用
    :param request:
    :return:
    '''
    error = ''
    login_form = user_form.UserInfo(request.POST)
    ret = {'login_obj': login_form, 'error': ''}
    if request.method == "POST":
        if not login_form.is_valid():
            ret['error'] = u'用户名或密码格式错误.'
            return render(request, 'auth/login.html', ret)
        else:
            data = login_form.clean()
            result = account_manager.check_valid(**data)        # 专门检测用户登录账户密码的方法
            if result.status:
                ret = {'id': result.data.user_info.id, 'name': result.data.user_info.name,
                       'weight': result.data.user_info.user_type.code}
                request.session['auth_user'] = json.dumps(ret)
                target = request.GET.get('back', '/')
                print "Login  successful!!!!!!"
                return redirect(target)
            else:
                error = '用户名或密码错误.'
    return render(request, 'auth/login.html', {'error': error, 'login_obj': login_form})


def logout(request):
    '''
    老的注销方法  已弃用
    :param request:
    :return:
    '''
    del request.session['auth_user']
    request.username = ''
    return redirect('/account/login/')
































