#!/usr/bin/env python
# _*_coding:utf-8 _*_
from django.shortcuts import render, HttpResponse
from Daily_app.manage import iptables_manage
from Daily_app.manage import iptables_api_manager
from overall.auth.login_auth import login_auth
from Daily_app.views.account import login_sso
import json
# Create your views here.


def test(request):

    return HttpResponse('ewfwefwfwefwfwefwfwfew')


@login_sso
# @login_auth
def index(request):
    # return render(request, 'base/base.html', {'username': request.username})
    user_info = request.userinfo
    return render(request, 'base/base.html', {'userinfo': user_info})


@login_sso
def iptables_init(request):
    '''
    iptables初始化页面
    '''
    user_info = request.userinfo
    return render(request, 'iptables/iptables_init.html', {'userinfo': user_info})
    # return render(request, 'iptables/iptables_init.html')


@login_sso
def iptables_rules(request):
    '''
    获取初始化iptables规则
    '''
    ret = iptables_manage.get_all_rule_list().__dict__

    return HttpResponse(json.dumps(ret))


@login_sso
def iptables_init_execute(request):
    '''
    接受前端传送过来的初始化信息 去服务器执行
    '''
    if request.method == "POST":
        data = request.POST
        ret = iptables_manage.execute_init_rules(data, request).__dict__

        return HttpResponse(json.dumps(ret))


@login_sso
def iptables_check(request):
    '''
    展示主机下的iptables所有规则
    '''
    return render(request, 'iptables/iptables_check.html', )


@login_sso
def iptables_rules_check(request):
    '''
    获取某个服务器下的iptables规则
    :param request:
    :return:
    '''
    if request.method == "POST":
        data = request.POST
        ret = iptables_manage.get_host_rules(data).__dict__
        return HttpResponse(json.dumps(ret))


@login_sso
def iptables_rules_add(request):
    '''
    添加新的iptables规则
    '''

    return render(request, 'iptables/iptables_add.html')


@login_sso
def iptables_add_quick(request):
    '''
    添加新的iptables规则
    '''
    if request.method == "POST":
        data = request.POST
        ret = iptables_manage.add_rule_quick(data).__dict__

        return HttpResponse(json.dumps(ret))


@login_sso
def iptables_add_cmd(request):
    '''
    添加新的iptables规则
    '''
    if request.method == "POST":
        data = request.POST
        ret = iptables_manage.add_rule_str(data).__dict__

        return HttpResponse(json.dumps(ret))


def iptables_api(request):
    '''
    iptables总的api
    '''
    ret = {'status': '', 'message': '', 'other msg': '', 'result_data': ''}
    if request.method == "POST":
        # data = json.loads(request.POST.get('data'))     # 提交的数据
        data = request.body
        print "ppppppppppppppppppppost___data", data
        post_result = iptables_api_manager.handle_iptables_post_data(data)
        if post_result.status:
            ret['status'] = 'Successful'
            ret['other msg'] = post_result.other
            ret['result_data'] = post_result.data
        else:
            ret['status'] = 'Failed'
            ret['message'] = post_result.message

    else:
        d = dict(request.GET)
        for k, v in d.items():
            print k, v

    return HttpResponse(json.dumps(ret))






