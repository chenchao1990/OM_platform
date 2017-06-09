#!/usr/bin/env python
# _*_coding:utf-8 _*_

from overall.response.base_response import BaseResponse
from ansible_app.ansible_method.ansible_api import Ansible_API
from Daily_app.execute_cmd import pwd_query
from ansible_app.ansible_method.make_hosts import create_ansible_host_file
import json
import re

ipv4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){2}(\.(25[0-4]|2[0-4]\d|[0-1]?\d?\d))$')


def smtp_add(ip_list):
    '''
    接受前端传送额ip列表 然后将其添加到配置文件中
    '''
    response = BaseResponse()

    host_ip = ["10.58.47.39", "10.58.47.40"]
    try:
        ip_list = json.loads(ip_list)
        print "ip_____list", ip_list
        if len(ip_list) == 0:
            raise Exception(u'你总得输个IP地址吧！')
        error_ip = []
        for ip in ip_list:
            if not ipv4_re.match(str(ip)):
                error_ip.append(str(ip))
                # raise Exception(u'ip address error %s' % ip)
        print "error_ip_list", error_ip
        if len(error_ip) != 0:
            response.message = u'输入IP地址格式错误'
            return response
        smtp_cmd = make_add_smtp_cmd(ip_list)               # smtp执行的命令
        host_pwd_info = pwd_query.main(host_ip, [], "P")
        host_file_status = create_ansible_host_file(host_pwd_info, 'smtp_host')
        if not host_file_status.status:
            raise Exception('create ansible smtp host failed')

        ansible_obj = Ansible_API(host_file_status.data)
        ansible_obj.host = "smtp_host"
        run_cmd_resule = ansible_obj.shell_run(smtp_cmd)
        response.status = True
        response.data = run_cmd_resule
    except Exception, e:
        response.message = str(e.message)

    return response


def make_add_smtp_cmd(ip_list):
    '''
    制作添加smtp记录的命令
    '''
    smtp_cmd = "echo '%s    OK' >> /etc/postfix/source_address"
    reload_cmd = "postmap  /etc/postfix/source_address"
    cmd_list = []
    for ip in ip_list:
        new_cmd = smtp_cmd % ip
        cmd_list.append(new_cmd)
    cmd_list.append(reload_cmd)
    big_cmd = "  &&  ".join(cmd_list)
    print "cccccccccccccccccccccccccc", big_cmd
    return big_cmd
