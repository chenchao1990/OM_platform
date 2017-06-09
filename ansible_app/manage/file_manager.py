#!/usr/bin/env python
# _*_coding:utf-8 _*_

from ansible_app.ansible_method.ansible_api import Ansible_API
from overall.response.base_response import BaseResponse
from Daily_app.execute_cmd import pwd_query
from ansible_app.ansible_method.make_hosts import create_host_file
from ansible_app.manage import log_manager
import os
import time
import datetime
import xlrd
import re

ipv4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){2}(\.(25[0-4]|2[0-4]\d|[0-1]?\d?\d))$')


def upload_ip_file(file_obj, filename, ipfile_dir):
    '''
    接受上传的ip地址文件
    '''

    response = BaseResponse()
    try:
        # 保存上传的文件
        if not filename.endswith("xlsx"):
            response.message = u"文件格式错误"
            return response
        file_dir = ipfile_dir + filename
        f = open(file_dir, 'wb')
        for line in file_obj.chunks():              # 保存文件
            f.write(line)
        f.close()

        response.status = True
        response.message = u'上传成功'
        return response

    except Exception, e:
        response.message = str(e)
        return response


def upload_file(file_obj, script_file_dir):
    '''
    接受上传的文件
    '''

    response = BaseResponse()
    try:
        # 保存上传的脚本
        filename = file_obj.name
        file_dir = script_file_dir + filename
        f = open(file_dir, 'wb')
        for line in file_obj.chunks():              # 保存文件
            f.write(line)
        f.close()

        response.status = True
        response.message = u'上传成功'
        return response
    except AttributeError:
        response.message = u'选择上传文件'
        return response
    except Exception, e:
        print "up____error", str(e)
        response.message = str(e)
        return response


def get_upload_files(file_dir):
    '''
    获取ansible_tmp下所有的文件
    '''
    Kilobyte = 1000
    Megabyte = float(1000*Kilobyte)
    Gigabyte = float(1000*Megabyte)

    response = BaseResponse()
    try:
        file_list = []
        all_file_list = os.listdir(file_dir)
        for file_name in all_file_list:
            t_dict = {}
            # dt = datetime.datetime.strptime(pageTime, "%Y-%m-%d %H:%M:%S")
            file_path = os.path.join(file_dir, file_name.decode('utf8'))
            file_obj = os.stat(file_path)
            str_t = file_obj.st_ctime
            f_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(str_t))  # 文件修改时间
            change_time = datetime.datetime.strptime(f_time, "%Y-%m-%d %H:%M:%S")
            d = change_time + datetime.timedelta(hours=8)
            nTime = d.strftime("%Y-%m-%d %H:%M:%S")
            f_size = float(file_obj.st_size)
            if f_size < 1000000:
                f_size = str(f_size / Kilobyte) + 'KB'
            else:
                f_size = str(f_size/Megabyte) + 'MB'
            t_dict['filename'] = file_name.decode('utf8')
            t_dict['filesize'] = f_size
            t_dict['filetime'] = nTime
            file_list.append(t_dict)
        response.data = file_list
        response.status = True
        return response

    except Exception, e:
        response.message = str(e)
        return response


def send_file(file_dir, data, username):
    response = BaseResponse()
    try:
        # 开始读取文件中的内容
        filename = data.get('file_name', None)
        envir = data.get('envir', None)
        if envir is None:
            response.message = u'请检查所选环境'
            return response
        file_dir = file_dir + "host_ip.xlsx"
        is_have = os.path.isfile(file_dir)
        if not is_have:
            response.message = u'指定文件不存在'
            return response

        ip_info_dict = read_ip_from_file(file_dir)
        ip_list = ip_info_dict['ip_list']
        pwd_check = pwd_query.main(ip_list, ip_info_dict['ip_info_list'], envir)
        if len(pwd_check) == 0:
            response.pwd_state = False
            response.message = u"密码检测失败!!请检查所选环境和密码是否存在~"
            return response
        create_host_file(pwd_check)                     # 生成一个全新的hosts文件
        send_file_obj = Ansible_API()
        send_result = send_file_obj.send_file(filename)
        log_manager.ansible_file_log(username, ip_list, filename)
        no_pass_host = check_no_password_host(ip_list, pwd_check)

        response.no_pass = no_pass_host
        response.status = True
        response.data = send_result
        return response
    except Exception, e:
        response.message = str(e)
        return response


def run_script(script_dir, host_dir, data, username):
    '''
    调用API 和 上传的IP文件去运行脚本
    '''
    response = BaseResponse()
    try:
        # 开始读取文件中的内容
        script_name = data.get('script_name', None)
        envir = data.get('envir', None)
        if envir is None:
            response.message = u'请检查所选环境'
            return response
        host_path = host_dir + "host_ip.xlsx"
        is_have = os.path.isfile(host_path)
        if not is_have:
            response.message = u'指定IP文件不存在'
            return response
        script_path = script_dir + script_name
        script_have = os.path.isfile(script_path)
        if not script_have:
            response.message = u'脚本文件不存在'
            return response
        ip_info_dict = read_ip_from_file(host_path)
        ip_list = ip_info_dict['ip_list']
        pwd_check = pwd_query.main(ip_list, ip_info_dict['ip_info_list'], envir)
        if len(pwd_check) == 0:
            response.pwd_state = False
            response.message = u"密码检测失败!!请检查所选环境和密码是否存在~"
            return response
        no_pass_host = check_no_password_host(ip_list, pwd_check)
        create_host_file(pwd_check)                     # 生成一个全新的hosts文件
        send_file_obj = Ansible_API()
        send_result = send_file_obj.run_script(script_path)
        log_manager.ansible_script_log(username, ip_list, script_name)
        response.status = True
        response.no_pass = no_pass_host
        response.data = send_result
        return response
    except Exception, e:
        print "execute script error::: %s" % e
        response.message = str(e)
        return response


def check_no_password_host(all_ip_list, host_list):
    '''
    检查密码不存在的ip
    :param host_list:
    :return:
    '''
    result_ip_list = []
    for ip_dict in host_list:
        result_ip_list.append(ip_dict['ip'])
    s = list(set(all_ip_list) - set(result_ip_list))
    return s


def read_ip_from_file(file_dir):
    '''
    读取一个文件中内容
    '''

    try:
        info_dict = {'ip_list': [], 'ip_info_list': []}
        ip_list = []
        ip_info_list = []
        excel_obj = xlrd.open_workbook(file_dir)
        sheet = excel_obj.sheet_by_index(0)

        all_rows = sheet.nrows              # 表格中的总行数
        for line_num in range(0, all_rows):
            l = []
            current_list = sheet.row_values(line_num)           # 获取当前行的数据列表
            if len(current_list) == 0:
                continue
            if not ipv4_re.match(current_list[0]):
                continue
            if len(current_list) > 1:
                l.append(current_list[0])
                l.append(current_list[1])
            if len(current_list) == 1:
                l.append(current_list[0])
            ip_list.append(current_list[0])
            ip_info_list.append(l)
        info_dict['ip_list'] = ip_list
        info_dict['ip_info_list'] = ip_info_list
        return info_dict
    except Exception, e:
        print "read ip from file ERROR", e


def delete_upload_file(filename, file_dir):
    '''
    删除用户所选的文件
    '''
    response = BaseResponse()
    try:
        file_path = file_dir + filename
        if os.path.isfile(file_path):
            os.remove(file_path)
            response.status = True
            return response
        else:
            response.message = u'删除失败'
            return response
    except Exception, e:
        response.message = str(e)
        return response








