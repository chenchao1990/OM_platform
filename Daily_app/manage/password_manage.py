#!/usr/bin/env python
# _*_coding:utf-8 _*_
from overall.response.base_response import BaseResponse
from Daily_app.execute_cmd import pwd_query
from Daily_app.execute_cmd import pwd_query_file
from Daily_app.execute_cmd import pwd_import
from Daily_app.execute_cmd import revise_root_pwd
from Daily_app.execute_cmd import set_manage_pwd
from Daily_app.execute_cmd import change_bmc
from Daily_app.manage import log_manager
from overall.Task_Queue.RedisQueue import RedisQueue
import re
import os
import xlrd

ipv4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){2}(\.(25[0-4]|2[0-4]\d|[0-1]?\d?\d))$')


def password_check(data):

    response = BaseResponse()

    ip_list = data.get('ip_list', None)
    envir = data.get('envir', None)
    is_win = data.get('is_win', None)
    special_user = data.get('s_user', None)
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
        response.status = False
        response.message = u"IP地址出现错误!!!"
        return response

    set_host = list(set(host_ip))                           # 将列表去重
    if is_win == "true":
        t = True
    else:t = False
    pwd_check = pwd_query.main(set_host, [], envir, t, special_user)            # 调用密码API 获取密码的列表 *****

    if len(pwd_check) == 0:
        response.message = u"密码检测失败!!请检查所选环境和密码是否存在~"
        response.pwd_status = False
        return response

    response.status = True
    response.data = pwd_check
    return response


def upload_pwd_file(file_obj, filename, up_dir):
    '''
    将文件上传至目录下
    '''
    response = BaseResponse()
    try:
        # 保存上传的文件
        if not filename.endswith("xlsx"):
            response.message = u"文件格式错误"
            return response
        file_dir = up_dir + filename
        f = open(file_dir, 'wb')
        for line in file_obj.chunks():              # 保存文件
            f.write(line)
        f.close()

        response.status = True
        return response

    except Exception, e:
        response.message = str(e)
        return response


def get_pwd_file(file_dir):
    '''
    获取所有的上传pwd文件
    '''
    response = BaseResponse()

    try:
        file_list = []
        all_file_list = os.listdir(file_dir)
        for file_name in all_file_list:
            if file_name.endswith('xlsx'):
                file_list.append(file_name)          # 将正确格式的文件筛选出

        response.data = file_list
        response.status = True
        return response

    except Exception, e:
        response.message = str(e)
        return response


def get_server_file(file_dir):
    '''
    获取所有的上传pwd文件
    '''
    response = BaseResponse()

    try:
        file_list = []
        all_file_list = os.listdir(file_dir)
        for file_name in all_file_list:
            if file_name.endswith('xlsx'):
                file_list.append(file_name)          # 将正确格式的文件筛选出

        response.data = file_list
        response.status = True
        return response

    except Exception, e:
        response.message = str(e)
        return response


def delete_pwd_file(file_dir):
    '''
    删除所有的上传ping文件
    '''
    response = BaseResponse()

    try:
        all_file_list = os.listdir(file_dir)
        for file_name in all_file_list:
            os.remove(file_dir+file_name)
        # all_file_list2 = os.listdir(file_dir)
        response.status = True
        return response
    except Exception, e:
        response.message = str(e)
        return response


def file_check_pwd(data, up_dir):
    '''
    通过上传文件去检查密码
    '''

    response = BaseResponse()
    try:
        # 开始读取文件中的内容
        filename = data.get('file_name', None)
        envir = data.get('envir', None)
        if envir is None:
            response.message = u'请检查所选环境'
            return response
        file_dir = up_dir + filename
        is_have = os.path.isfile(file_dir)
        if not is_have:
            response.message = u'指定文件不存在'
            return response
        ip_info_dict = read_ip_from_file(file_dir)
        re_dict = pwd_query_file.main(ip_info_dict['ip_list'], ip_info_dict['all_ip_list'], envir)
        if re_dict['status'] == 'success':
            response.data = re_dict['result']
            response.status = True
            return response
        else:
            response.message = u'未知错误'
            response.status = False
            return response
    except Exception, e:
        response.message = str(e)
        return response


def file_import_pwd(data, up_dir, username):
    '''
    通过上传文件 导入密码
    '''

    response = BaseResponse()
    try:
        # 开始读取文件中的内容
        filename = data.get('file_name', None)
        envir = data.get('envir', None)
        if envir is None:
            response.message = u'请检查所选环境'
            return response
        file_dir = up_dir + filename
        is_have = os.path.isfile(file_dir)
        if not is_have:
            response.message = u'指定文件不存在'
            return response
        ip_info_dict = read_pwd_from_file(file_dir)     # 将ip信息从文件中读取出来
        re_dict = pwd_import.main(ip_info_dict['ip_list'], ip_info_dict['all_ip_data'], envir)
        if re_dict['import_re']:
            log_manager.import_password_log(username, ip_info_dict['ip_list'], 'success', 'only_import')      # 写入日志
            response.status = True
            response.data = u'导入成功'
            return response
        else:
            log_manager.import_password_log(username, ip_info_dict['ip_list'], 'fail', 'only_import')      # 写入日志
            response.message = u"密码导入失败: %s" % re_dict['message']
            response.status = False
            return response
    except Exception, e:
        print e
        response.message = str(e)
        return response


def change_pwd_and_save(data, up_dir, username):
    '''
    通过上传文件 导入密码
    '''

    response = BaseResponse()
    final_dict = {'change_re': None, 'save_re': None, 'queue_key': None}
    try:
        # 开始读取文件中的内容
        filename = data.get('file_name', None)
        envir = data.get('envir', None)
        if envir is None:
            response.message = u'请检查所选环境'
            return response
        file_dir = up_dir + filename.encode('utf8')
        is_have = os.path.isfile(file_dir)
        if not is_have:
            response.message = u'指定文件不存在'
            return response
        ip_info_dict = read_change_info(file_dir)           # 从文件中读取的密码数据

        change_re_list, queue_name = revise_root_pwd.change_host_pwd(ip_info_dict['all_info_list'])     # 调取脚本 修改密码

        # change_obj = change_root_pwd.ChangePassword()     # 调取脚本 修改密码
        # change_re_list = change_obj.change_host_pwd(ip_info_dict['all_info_list'])
        # print "iiiiiiiiiiiddddddddddddddddddd", change_obj.name
        print "change_re_list", change_re_list
        final_dict['change_re'] = change_re_list
        final_dict['queue_key'] = queue_name
        s = ip_info_dict['all_info_list']
        for i in s:
            i.pop(2)
        save_dict = pwd_import.main(ip_info_dict['ip_list'], ip_info_dict['all_info_list'], envir)      # 保存密码
        print "password_save result", save_dict
        final_dict['save_re'] = save_dict

        log_manager.import_password_log(username, ip_info_dict['ip_list'], 'success', 'change_host')
        response.data = final_dict
        response.status = True
        return response
    except Exception, e:
        # log_manager.import_password_log(username, ip_info_dict['ip_list'], 'fail', 'change_host')
        response.message = str(e)
        print str(e)
        return response


def change_manager_pwd(data, manage_pwd_dir, username):
    '''
    修改管理口的密码
    '''

    response = BaseResponse()
    final_dict = {'change_re': None, 'save_re': None}
    try:
        # 开始读取文件中的内容
        filename = data.get('file_name', None)

        file_dir = manage_pwd_dir + filename.encode('utf8')
        is_have = os.path.isfile(file_dir)
        if not is_have:
            response.message = u'指定文件不存在'
            return response
        ip_info_dict = read_change_info(file_dir)           # 从文件中读取的密码数据
        change_re_list = set_manage_pwd.change_manage_pwd(ip_info_dict['all_info_list'])     # 执行修改密码的命令方法
        final_dict['change_re'] = change_re_list
        s = ip_info_dict['all_info_list']
        for i in s:
            i.pop(2)

        # log_manager.import_password_log(username, ip_info_dict['ip_list'], 'success', 'change_manage_pwd')
        response.data = final_dict
        response.status = True
        return response
    except Exception, e:
        # log_manager.import_password_log(username, ip_info_dict['ip_list'], 'fail', 'change_manage_pwd')
        response.message = str(e)
        print str(e)
        return response


def read_ip_from_file(file_dir):
    '''
    读取一个文件中内容
    '''
    try:
        ip_info = {'all_ip_list': None, 'ip_list': None}
        all_ip_list = []
        ip_list = []
        excel_obj = xlrd.open_workbook(file_dir)
        sheet = excel_obj.sheet_by_index(0)

        all_rows = sheet.nrows              # 表格中的总行数
        for line_num in range(0, all_rows):
            current_list = sheet.row_values(line_num)           # 获取当前行的数据列表
            if len(current_list) == 0:
                continue
            if not ipv4_re.match(current_list[0]):
                continue
            if not current_list[1]:
                current_list[1] = 'root'
            ip_list.append(current_list[0])
            all_ip_list.append(current_list)
        ip_info['all_ip_list'] = all_ip_list
        ip_info['ip_list'] = ip_list
        return ip_info
    except Exception, e:
        print "read_ip_from_file", e


def read_pwd_from_file(file_dir):
    '''
    读取文件中的密码 用于导入
    '''
    try:
        ip_info = {'all_ip_data': None, 'ip_list': None}
        all_ip_list = []
        ip_list = []
        excel_obj = xlrd.open_workbook(file_dir)
        sheet = excel_obj.sheet_by_index(0)
        all_rows = sheet.nrows              # 表格中的总行数
        for line_num in range(0, all_rows):
            current_list = sheet.row_values(line_num)           # 获取当前行的数据列表
            if len(current_list) == 0:
                continue
            if not ipv4_re.match(current_list[0]):
                continue
            if not current_list[1]:                     # 用户
                current_list[1] = 'root'
            if current_list[2]:                         # 新密码
                pwd = str(current_list[2])
                new_pwd = re.sub("\'", '*', pwd)
                current_list[2] = new_pwd
            else:
                continue
            ip_list.append(current_list[0])         # 将所有IP地址归类
            all_ip_list.append(current_list)        # 将所有的密码数据归类
        ip_info['all_ip_data'] = all_ip_list
        ip_info['ip_list'] = ip_list
        return ip_info
    except Exception, e:
        print e


def read_change_info(file_dir):
    '''
    读取表格中的信息  用户登陆系统修改密码
    '''
    try:
        ip_info = {'all_info_list': None, 'ip_list': None}
        ip_info_list = []
        ip_list = []
        excel_obj = xlrd.open_workbook(file_dir)
        sheet = excel_obj.sheet_by_index(0)

        all_rows = sheet.nrows              # 表格中的总行数
        for line_num in range(0, all_rows):
            current_list = sheet.row_values(line_num)           # 获取当前行的数据列表
            print "current_______list", current_list
            if len(current_list) == 0:
                continue
            if not ipv4_re.match(current_list[0].strip()):
                continue
            if not current_list[1]:
                continue
            if not current_list[2]:
                continue
            if current_list[3]:                 # 新密码

                pwd = current_list[3]
                # pwd = re.sub("\'", '*', pwd)
                current_list[3] = pwd

            else:
                continue
            if type(current_list[2]) == float:      # 如果密码是浮点数 将其转换
                current_list[2] = str(int(current_list[2]))
            if type(current_list[3]) == float:
                current_list[3] = str(int(current_list[3]))
            for i, v in enumerate(current_list):
                current_list[i] = current_list[i].strip()

            print "new_current_list", current_list
            ip_list.append(current_list[0].strip())
            ip_info_list.append(current_list)
        ip_info['all_info_list'] = ip_info_list
        ip_info['ip_list'] = ip_list
        return ip_info
    except Exception, e:
        print e


def change_server_password(data, up_dir, username):
    '''
    通过读取上传的host文件 修改BMC管理口密码
    '''

    response = BaseResponse()
    final_dict = {'change_re': None, 'save_re': None}
    try:
        # 开始读取文件中的内容
        filename = data.get('file_name', None)

        file_dir = up_dir + filename.encode('utf8')
        is_have = os.path.isfile(file_dir)
        if not is_have:
            response.message = u'指定文件不存在'
            return response
        ip_info_dict = read_change_info(file_dir)           # 从文件中读取的密码数据
        # change_obj = change_bmc.ManageBMC(ip_info_dict['all_info_list'])     # 调取脚本 修改密码
        # change_re_list = change_obj.run_change_pwd()
        change_re_list = change_bmc.change_bmc_password(ip_info_dict['all_info_list'])
        final_dict['change_re'] = change_re_list
        response.data = final_dict
        response.status = True
        return response
    except Exception, e:
        # log_manager.import_password_log(username, ip_info_dict['ip_list'], 'fail', 'change_host')
        response.message = str(e)
        print str(e)
        return response


def get_data_from_redis(data):
    '''
    从redis里获取队列中的数据
    '''
    response = BaseResponse()
    re_list = []
    try:
        queue_key = data.get('queue_key', None)     # 取出前端提交的queue name
        if not queue_key:
            raise Exception('not found queue key in post data.')
        q_obj = RedisQueue(queue_key)
        queue_size = q_obj.qsize()
        q_re = q_obj.get_all()       # 取出队列中现存的所有数据

        for i in q_re:
            re_list.append(eval(i))
        print "qqqqqqqqqqqqqqqqqqq", q_re, type(q_re)
        response.data = re_list
        response.q_size = queue_size
        response.status = True
    except Exception, e:
        response.message = e.message
    return response






























