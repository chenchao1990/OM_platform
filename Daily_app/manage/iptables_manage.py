#!/usr/bin/env python
# _*_coding:utf-8 _*_
from overall.response.base_response import IptablesCheck
from overall.response.base_response import BaseResponse
from Daily_app.model_handle import iptables_handle
from Daily_app.execute_cmd import pwd_query
from Daily_app.execute_cmd import execute_iptables
from Daily_app.manage import iptableslog_manager
import json
import re


def get_all_rule_list():
    response = BaseResponse()

    try:
        ret = iptables_handle.get_all_rules()
        response.status = 1
        response.data = list(ret)
    except Exception, e:
        response.message = str(e)
    return response


def execute_init_rules(data, request):
    '''
    执行初始化的iptables规则
    1、获取IP
    2、确认环境
    3、根据环境和IP去获取密码

    4、根绝前端规则ID表，来确认规则的条数，然后获取到初始化表中的规则
    5、登陆服务器 执行添加规则命令
    6、确认规则已经生效
    7、返回执行的状态
    '''
    response = IptablesCheck()

    ip_list = data.get('ip_list', None)
    envir = data.get('envir', None)
    rule_id_list = data.get('rule_id_list', None)
    rule_id_list = json.loads(rule_id_list)
    value_list = [ip_list, envir, rule_id_list]
    for i in value_list:
        if i is None:
            response.message = u'请检查提交的数据'
            return response

    ipv4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
    error_ip = []
    host_ip = ip_list.strip().split(",")
    for ip in host_ip:
        if not ipv4_re.match(ip.strip()):
            error_ip.append(ip)
    print "error_--------------ip", error_ip
    if len(error_ip) > 0:
        response.host_ip = error_ip
        response.ip_status = False
        response.message = u"IP地址出现错误!!!"
        return response

    set_host = list(set(host_ip))                           # 将列表去重
    pwd_check = pwd_query.main(set_host, [], envir)            # 调用密码API 获取密码的列表 *****

    if len(pwd_check) == 0:
        response.message = u"密码检测失败!!请检查所选环境和密码是否存在~"
        response.pwd_status = False
        return response
    # 获取iptables初始的规则  根据前端传递的ID列表
    rule_list = iptables_handle.get_rules_by_ids(rule_id_list)              # 获取所有ID的规则
    rule_str_list = []                                                      # 将规则添加到列表中
    for i in rule_list:
        rule_str_list.append(str(i))

    re_list = []                                    # 存放每台IP的执行结果
    for host_info in pwd_check:
        ip = host_info['ip']
        pwd = host_info['pwd']
        iptables_obj = execute_iptables.RunIptables(rule_str_list, ip, pwd)
        exe_re = iptables_obj.execute_iptables()
        re_list.append(exe_re)

    iptableslog_manager.iptables_init_log(request.userinfo.get('cn_name'),
                                          request.userinfo.get('user_id'),
                                          ip_list)   # 将初始化记录写入日志
    response.status = True
    response.data = re_list
    return response


def get_host_rules(data):
    '''
    获取主机下的所有iptables规则
    :param data:
    :return:
    '''
    response = BaseResponse()

    ip_list = data.get('ip_list', None)             # 输入的IP地址
    envir = data.get('envir', None)                 # 环境

    value_list = [ip_list, envir]
    for i in value_list:
        if i is None:
            response.message = u'请检查提交的数据'
            return response

    ipv4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
    error_ip = []
    host_ip = ip_list.strip().split(",")

    for ip in host_ip:
        if not ipv4_re.match(ip):
            error_ip.append(ip)
    if len(error_ip) > 0:
        response.host_ip = error_ip
        response.ip_status = False
        response.message = u"IP地址出现错误!!!"
        return response

    set_host = list(set(host_ip))                           # 将列表去重
    pwd_check = pwd_query.main(set_host, [], envir)            # 调用密码API 获取密码的列表 *****

    if len(pwd_check) == 0:
        response.message = u"密码检测失败!!请检查所选环境和密码是否存在~"
        response.pwd_status = False
        return response

    re_list = []                                    # 存放每台IP的执行结果
    for host_info in pwd_check:
        ip = host_info['ip']
        pwd = host_info['pwd']
        iptables_obj = execute_iptables.RunIptables([], ip, pwd)            # 连接服务器对象
        exe_re = iptables_obj.get_all_rules()                               # 获取规则的方法
        re_list.append(exe_re)
    response.data = re_list
    response.status = True
    return response


def make_rules(ip_list, tag):
    rule_list = []
    rule_str = iptables_handle.get_quick_rule(tag)
    for ip in ip_list:
        new_rule = str(rule_str) % ip
        rule_list.append(new_rule)
    return rule_list


def add_rule_quick(data):
    '''
    获取主机下的所有iptables规则
    :param data:
    :return:
    '''
    response = BaseResponse()

    ip_list = data.get('ip_list', None)             # 输入的IP地址
    envir = data.get('envir', None)                 # 环境
    rule_ips = data.get('rule_ips')                 # 要添加的规则IP
    rule_ips = json.loads(rule_ips)

    value_list = [ip_list, envir]
    for i in value_list:
        if i is None:
            response.message = u'请检查提交的数据是否为空'
            return response

    ipv4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
    error_ip = []
    host_ip = ip_list.strip().split(",")

    for ip in host_ip:
        if not ipv4_re.match(ip):
            error_ip.append(ip)
    if len(error_ip) > 0:
        response.host_ip = error_ip
        response.ip_status = False
        response.message = u"IP地址出现错误!!!"
        return response

    set_host = list(set(host_ip))                           # 将列表去重
    pwd_check = pwd_query.main(set_host, [], envir)            # 调用密码API 获取密码的列表 *****

    if len(pwd_check) == 0:
        response.message = u"密码检测失败!!请检查所选环境和密码是否存在~"
        response.pwd_status = False
        return response

    re_list = []                                    # 存放每台IP的执行结果
    all_input_ip = []
    tag_str = None
    # 将输入的规则IP 和 对应类型的规则拼接在一起
    if len(rule_ips) > 0:

        tag_str = rule_ips[0].get('rule_type')
        for value in rule_ips:
            all_input_ip.append(value['ip'])
    rule_list = make_rules(all_input_ip, tag_str)
    for host_info in pwd_check:
        ip = host_info['ip']
        pwd = host_info['pwd']
        iptables_obj = execute_iptables.RunIptables(rule_list, ip, pwd)            # 连接服务器对象
        exe_re = iptables_obj.execute_iptables()                                     # 获取规则的方法
        re_list.append(exe_re)
    response.data = re_list
    response.status = True
    return response


def add_rule_str(data):
    '''
    获取主机下的所有iptables规则
    :param data:
    :return:
    '''
    response = BaseResponse()

    ip_list = data.get('ip_list', None)             # 输入的IP地址
    envir = data.get('envir', None)                 # 环境
    rule_cmd_list = data.get('rule_cmd_list')                 # 要添加的规则IP
    rule_cmd_list = json.loads(rule_cmd_list)

    value_list = [ip_list, envir]
    for i in value_list:
        if i is None:
            response.message = u'请检查提交的数据是否为空'
            return response

    ipv4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
    error_ip = []
    host_ip = ip_list.strip().split(",")

    for ip in host_ip:
        if not ipv4_re.match(ip):
            error_ip.append(ip.strip())
    if len(error_ip) > 0:
        response.host_ip = error_ip
        response.ip_status = False
        response.message = u"IP地址出现错误!!!"
        return response

    set_host = list(set(host_ip))                           # 将列表去重
    pwd_check = pwd_query.main(set_host, [], envir)            # 调用密码API 获取密码的列表 *****

    if len(pwd_check) == 0:
        response.message = u"密码检测失败!!请检查所选环境和密码是否存在~"
        response.pwd_status = False
        return response

    re_list = []                                    # 存放每台IP的执行结果
    all_cmd_list = []
    error_list = []
    # 将输入的规则IP 和 对应类型的规则拼接在一起
    if len(rule_cmd_list) > 0:

        for cmd_str in rule_cmd_list:
            if cmd_str.strip().startswith('iptables'):
                all_cmd_list.append(cmd_str)
            else:
                error_list.append(cmd_str)
    if len(error_list) > 0:
        response.message = u"命令输入错误，请检查。 %s " % ",".join(error_list)
        response.cmd_status = False
        return response
    for host_info in pwd_check:
        ip = host_info['ip']
        pwd = host_info['pwd']
        iptables_obj = execute_iptables.RunIptables(all_cmd_list, ip, pwd)            # 连接服务器对象
        exe_re = iptables_obj.execute_iptables()                                     # 获取规则的方法
        re_list.append(exe_re)
    response.data = re_list
    response.status = True
    return response


def get_log_count():
    '''
    获取iptables日志总条数
    :return:
    '''

    response = BaseResponse()
    try:
        result = iptables_handle.get_log_lists_count()         # j将搜索条件Q 传入其中 取出搜索到的数据的条数
        response.data = result
        response.status = True
    except Exception, e:
        response.message = str(e)

    return response


def get_log_lists(page_start, page_stop):
    '''
    获取指定条数的日志记录
    '''
    response = BaseResponse()
    try:
        values = ['id', 'log_type__type_name', 'login_user', 'user_num', 'msg',  'add_time']      # 在这里定义好查询表时 需要筛选的字段

        result = iptables_handle.get_log_list(page_start, page_stop, values)    # 搜索工单信息
        result = list(result)
        response.data = result                  # 封装到对象中
        response.status = True
    except Exception, e:
        response.message = str(e)

    return response


















