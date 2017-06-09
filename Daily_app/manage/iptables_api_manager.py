#!/usr/bin/env python
# _*_coding:utf-8 _*_

import json
from Daily_app.models import user_models
from overall.response.base_response import BaseResponse
from ansible_app.ansible_method.ansible_api import Ansible_API
from ansible_app.ansible_method.make_hosts import create_iptables_host_file
from Daily_app.execute_cmd import pwd_query_no_envir
from OM_platform import settings
import datetime


def handle_iptables_post_data(data):
    '''
    验证用户
    根据type去寻找分配适应的处理方法
    '''
    response = BaseResponse()

    try:
        post_data = json.loads(data)           # 提交的数据
        check_response = check_user_info(post_data)     # 验证用户的结果

        if not check_response.status:                   # 验证失败
            raise Exception('Authentication failed.')
        user = post_data['user']
        rule_type = post_data['type']
        # envir = post_data['envir']

        if not rule_type:                   # 验证失败
            raise Exception("'rule type' cannot be empty.")

        # if not envir:                   # 验证失败
        #     print "'envir' cannot be empty."
        #     raise Exception("'envir' cannot be empty.")
        rule_status = fix_rule_type(post_data['rules'], rule_type.strip(), user)

        if not rule_status.status:
            raise Exception(rule_status.message)
        response.other = rule_status.other
        response.data = rule_status.data
        response.status = True

    except Exception, e:
        print "handle_iptables_post_data Error", e
        response.message = e.message
    return response


def check_user_info(post_data):
    '''
    检查用户的信息
    '''
    response = BaseResponse()
    try:

        user = post_data['user']
        ip = post_data['ip']
        user_key = post_data['p_key']
        user_dict = {'user': user, 'ip': ip, 'p_key': user_key}

        ret = user_models.IptablesAuth.objects.filter(**user_dict).first()
        if not ret:
            raise Exception('Not found this user info, Authentication failed.')
        response.status = True
    except Exception, e:
        response.message = e.message
    response.user = user
    return response


def fix_rule_type(rule_data_list, rule_type, user):
    '''
    处理iptables字典数据 生成规则
    '''

    response = BaseResponse()

    try:
        if rule_type == 'easy':         # 如果规则是简单快速规则
            easy_result = easy_rules(rule_data_list, user)

            if not easy_result.status:
                raise Exception(easy_result.message)
            response.other = easy_result.other
            response.data = easy_result.data
        elif rule_type.strip() == 'normal':
            normal_result = NormalRule.process(rule_data_list, user)
            if not normal_result.status:
                raise Exception(normal_result.message)
            response.data = normal_result.data
        else:
            raise Exception("rule type is Error.")
        response.status = True
    except Exception, e:
        response.message = e.message
    return response


def easy_rules(rule_data, user):
    '''
    生成简单的规则
    '''
    response = BaseResponse()

    try:
        host_ip = rule_data['host_ip']
        rule_ip = rule_data['rule_ip']
        action = rule_data['action']

        if len(host_ip) == 0:
            raise Exception('host ip cannot be empty ')
        if len(rule_ip) == 0:
            raise Exception('rule ip cannot be empty ')
        if not action:
            raise Exception('action cannot be empty ')

        if action == "add":
            add_result = add_rule(host_ip, rule_ip, user)
            if not add_result.status:
                raise Exception(add_result.message)
            response.other = add_result.other
            response.data = add_result.data

        elif action == "delete":
            delete_result = delete_rule(host_ip, rule_ip, user)
            if not delete_result.status:
                raise Exception(delete_result.message)
            response.data = delete_result.data
            response.other = delete_result.other
        else:
            raise Exception("action is Error. 'add' or 'delete'")
        response.status = True
    except Exception, e:
        response.status = False
        response.message = e.message
    return response


# def normal_rule(rule_data, user):
#     '''
#     常规的规则
#     '''
class NormalRule(object):
    '''
    常规的规则处理
    '''

    @staticmethod
    def process(rule_data, user):       # 提交的字典数据中 rule那部门字典
        response = BaseResponse()
        try:
            _table = rule_data['table']         # 规则的 -t 参数
            _command = rule_data['command']     # 规则的操作  -A  -I  -D
            _chain = rule_data['chain']         # 规则对哪个链生效  INPUT OUTPUT
            _parameter = rule_data['parameter']     # 规则过滤的参数  -p -s -d -i -o 这是一个字典
            _option = rule_data['option']       # 规则的-j 参数 DROP ACCEPT REJECT
            # _action = rule_data['action']       # 规则的操作  添加  删除
            hosts = rule_data['hosts']
            new_iptables_cmd = ''

            if _table:
                table = ' -t ' + _table
            else:
                table = '-t filter'
            if _command:
                command = ' -%s ' % _command
            else:
                command = ' -A '
            if _chain:
                chain = ' %s ' % _chain
            else:
                chain = ' INPUT '
            if _option:
                option = ' -j %s ' % _option
            else:
                option = ' -j ACCEPT '
            new_iptables_cmd = 'iptables ' + table + command + chain
            print "mmmmmmmmmmmmmmmmmmmmmmmmmm", new_iptables_cmd
            if not _parameter:
                raise Exception("parameter must be have. eg: '-s 192.168.1.1/24 -d 10.58.60.1/24 -p tcp --port 22")
            _source = _parameter['source']
            _destination = _parameter['destination']
            _protocol = _parameter['protocol']
            _dport = _parameter['dport']
            _sport = _parameter['sport']
            _in = _parameter['in']
            _out = _parameter['out']

            if _source:
                source = ' -s '+','.join(_source)
            else: source = ''
            if _destination:
                destination = ' -d ' + ','.join(_destination)
            else:destination = ''
            if _protocol:
                protocol = ' -p ' + _protocol
            else: protocol = ''
            if _dport:
                dport = ' --dport ' + _dport
            else: dport = ''
            if _sport:
                sport = ' --sport ' + _sport
            else: sport = ''
            if _in:
                in_eth = ' -i ' + _in
            else: in_eth = ''
            if _out:
                out_eth = ' -o ' + _out
            else: out_eth = ''
            new_iptables_cmd = new_iptables_cmd + source + destination + protocol + dport + sport + in_eth + out_eth + option
            new_iptables_cmd = new_iptables_cmd + "  &&  service iptables save"
            print "nnnnnnnnnnnew_cmd------", new_iptables_cmd
            run_statue = run_iptables_cmd(hosts, new_iptables_cmd)
            if not run_statue.status:
                raise Exception(run_statue.message)

            response.status = True
            response.other = run_statue.other
            response.data = run_statue.data
        except Exception, e:
            print "eeeeeeeeeeeeeeeeeeeee normal", e
            response.message = e.message
        return response


def add_rule(host_ip, rule_ip, user):
    '''
    新增规则
    生成添加规则的命令列表
    将命令传递给 添加规则的方法去执行命令
    '''
    response = BaseResponse()
    try:
        make_rule_status = make_easy_rule(rule_ip)
        if not make_rule_status.status:
            raise Exception('make rule failed')
        # run_statue = run_iptables_script(host_ip, make_rule_status.data, user)        # 调用ansible执行iptables命令
        run_statue = run_iptables_cmd(host_ip, make_rule_status.data)                   # 调用ansible执行iptables命令
        if not run_statue.status:
            raise Exception("execute iptables command error")
        response.status = True
        response.other = run_statue.other
        response.data = run_statue.data
    except Exception, e:
        print "add_rule error", e
        response.message = e.message
    return response


def delete_rule(host_ip, rule_ip, user):
    '''
    删除规则
    生成添加规则的命令列表
    执行删除规则的命令
    '''
    response = BaseResponse()
    try:
        make_delete_status = make_delete_rule(host_ip, rule_ip)
        if not make_delete_status.status:
            raise Exception('make rule failed')
        # run_statue = run_iptables_script(host_ip, make_delete_status.data, user)        # 调用ansible执行iptables命令
        run_statue = run_iptables_cmd(host_ip, make_delete_status.data)        # 调用ansible执行iptables命令
        if not run_statue.status:
            raise Exception("execute iptables command error")
        response.status = True
        response.data = run_statue.data
        response.other = run_statue.other
    except Exception, e:
        print "delete_rule error", e
        response.message = e.message
    return response


def make_easy_rule(rule_ips):
    '''
    制作简单规则的命令字符串列表
    '''
    cmd_list = []
    easy_rule_cmd = "iptables -A INPUT -s %s -j ACCEPT"
    save_cmd = "service iptables save"
    response = BaseResponse()
    try:

        for rule_ip in rule_ips:
            cmd_list.append(easy_rule_cmd % rule_ip)
        cmd_list.append(save_cmd)
        response.status = True
        response.data = cmd_list
    except Exception, e:
        response.message = str(e)
    return response


def make_delete_rule(host_ips, rule_ips):
    '''
    制作简单规则
    '''
    cmd_list = []
    easy_rule_cmd = "iptables -D INPUT -s %s -j ACCEPT"
    save_cmd = "service iptables save"
    response = BaseResponse()
    try:

        for rule_ip in rule_ips:
            cmd_list.append(easy_rule_cmd % rule_ip)
        cmd_list.append(save_cmd)
        response.status = True
        response.data = cmd_list
    except Exception, e:
        response.message = str(e)
    return response


def run_iptables_cmd(host_ip, rule_cmd_list):
    '''
    查询主机列表的用户名和密码
    调用ansible API执行iptables的命令
    '''
    response = BaseResponse()
    try:
        pwd_info_list = pwd_query_no_envir.main(host_ip, [])          # 查询host 密码 用户名 对结果要进行对比分析
        no_found_ip_list = check_query_reuslt(host_ip, pwd_info_list)

        host_file_status = create_iptables_host_file(pwd_info_list)                    # 创建ansible host文件
        if not host_file_status:
            raise Exception("ansible iptables host file create failed")
        if isinstance(rule_cmd_list, list):
            rule_cmd = make_iptables_cmd(rule_cmd_list)
        else:
            rule_cmd = rule_cmd_list

        ansible_obj = Ansible_API(host_file_status.data)
        ansible_obj.host = 'iptables'
        run_cmd_result = ansible_obj.shell_run(rule_cmd)
        for k, e in run_cmd_result.items():
            print k, "--------------------", e
        if len(no_found_ip_list) != 0:
            response.other = "host %s is not found password" % " ".join(no_found_ip_list)
        response.status = True
        response.data = run_cmd_result

    except Exception, e:
        print "run_iptables_cmd Error: ", e
        response.message = str(e)

    return response


def run_iptables_script(host_ip, rule_cmd_list, user):
    '''
    查询主机列表的用户名和密码
    调用ansible API执行iptables的命令
    '''
    response = BaseResponse()
    try:
        host_pwd_info = pwd_query_no_envir.main(host_ip, [])          # 查询host 密码 用户名
        host_file_status = create_iptables_host_file(host_pwd_info)                    # 创建ansible host文件
        if not host_file_status:
            raise Exception("ansible iptables host file create failed")
        cmd_script = make_iptables_script(rule_cmd_list, user)
        if not cmd_script:
            raise Exception("create iptables command script failed")
        ansible_obj = Ansible_API(host_file_status.data)
        ansible_obj.host = "iptables"
        run_cmd_result = ansible_obj.run_script(cmd_script.data)

        response.status = True

    except Exception, e:
        print "run_iptables_cmd Error: ", e
        response.message = str(e)

    return response


def make_iptables_script(cmd_list, user):
    '''
    生成执行iptables命令的脚本
    '''
    response = BaseResponse()
    script_dir = settings.IPTABLES_SCRIPTS

    try:

        now_time = str(datetime.datetime.now())
        w = now_time.split(".")[0].replace(":", "_").split(" ")
        w.append(user+".sh")
        script_path = script_dir + "_".join(w)
        with open(script_path, 'w') as file_obj:
            for i in cmd_list:
                file_obj.write(i+"\n")

        response.status = True
        response.data = script_path
    except Exception, e:
        response.message = e.message

    return response


def make_iptables_cmd(rule_list):
    '''
    制作iptables命令字符串
    '''
    iptables_cmd = "  &&  ".join(rule_list)
    return iptables_cmd


def check_query_reuslt(host_ip, pwd_info_list):
    '''
    对比获取密码的的Ip
    '''

    for host in pwd_info_list:
        if host['ip'] in host_ip:
            host_ip.pop(host_ip.index(host['ip']))

    return host_ip
