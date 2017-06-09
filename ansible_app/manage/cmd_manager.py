#!/usr/bin/env python
# _*_coding:utf-8 _*_

from ansible_app.ansible_method.ansible_api import Ansible_API
from ansible_app.ansible_method.make_hosts import create_host_file
from overall.response.base_response import AnsibleResponse
from Daily_app.execute_cmd import pwd_query
from ansible_app.manage import log_manager

import re


def cmd_execute(data, username):
    '''
    执行命令
    '''
    response = AnsibleResponse()
    try:
        ip_list = data.get('ip_list', None)
        envir = data.get('envir', None)
        cmd = data.get('cmd', None)
        value_list = [ip_list, envir, cmd]

        for i in value_list:
            if not i:
                response.message = u'请检查提交的数据'
                return response

        ipv4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
        error_ip = []
        # host_ip = ip_list.strip().split(",")
        host_ip = [i.strip() for i in ip_list.strip().split(",")]
        for ip in host_ip:
            if not ipv4_re.match(ip.strip()):
                error_ip.append(ip.strip())

        if len(error_ip) > 0:
            response.status = False
            response.ip_state = False
            response.message = u"IP地址出现错误!!!"
            return response
        set_host = list(set(host_ip))                                   # 将列表去重
        pwd_check = pwd_query.main(set_host, [],  envir)            # 调用密码API 获取密码的列表 *****

        # w = [{'ip': '192.168.1.1', 'pwd': 'werg344wv23f56h56', 'user': 'root'}]
        if len(pwd_check) == 0:
            response.pwd_state = False
            response.message = u"密码检测失败!!请检查所选环境和密码是否存在~"
            return response
        check_re = []
        for ip_dict in pwd_check:
            check_re.append(ip_dict['ip'])
        no_pass_list = set(set_host) ^ set(check_re)
        # deny_cmd = ['reboot', 'rm', 'shutdown', 'half', 'mkfs', 'init']
        deny_cmd = ['reboot', 'shutdown', 'half', 'mkfs']
        for i in deny_cmd:
            if i in cmd:
                response.cmd_state = False
                response.message = u"输入的命令含有非法字符串 '%s'" % i
                return response
        create_host_file(pwd_check)                     # 生成一个全新的hosts文件
        cmd_obj = Ansible_API()
        cmd_result = cmd_obj.shell_run(cmd)
        log_manager.ansible_shell_log(username, set_host, cmd)
        response.status = True
        response.data = cmd_result
        if len(no_pass_list) > 0:
            response.no_pass = u'密码查询失败:  %s'  % ", ".join(no_pass_list)
        return response
    except Exception, e:
        response.message = str(e)

        return response

