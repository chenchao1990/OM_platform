#!/usr/bin/env python
# _*_coding:utf-8 _*_

from overall.response.base_response import BaseResponse
from Daily_app.execute_cmd import ping_host_ip
import json
import re
import xlrd
import os

ipv4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){2}(\.(25[0-4]|2[0-4]\d|[0-1]?\d?\d))$')
# ipv4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')


def single_ping(ip_data):

    response = BaseResponse()
    try:
        ip_list = json.loads(ip_data)
        # 先将输入的空ip去除
        for i, ip in enumerate(ip_list):
            if len(ip) == 0:
                ip_list.pop(i)
        # 检测ip输入不匹配
        error_ip = []
        for ip in ip_list:
            if not ipv4_re.match(ip):
                error_ip.append(ip)
        if len(error_ip) > 0:               # 说明IP地址有输入错误的 返回错误
            response.status = False
            response.message = u"IP地址输入错误 %s" % ",".join(error_ip)
            return response

        # ip地址输入正确，开始处理ping
        re_list = ping_host_ip.run_ping_by_ip(ip_list)

        response.data = re_list
        response.status = True
        return response
    except Exception, e:
        response.message = str(e)
        return response


def rang_ping(ip_data):

    response = BaseResponse()
    try:
        ip_dict = json.loads(ip_data)
        start_ip = ip_dict["start_ip"].strip()
        end_ip = ip_dict["end_ip"].strip()
        if len(start_ip) == 0 or len(end_ip) == 0:
            response.message = u"Ip地址输入错误"
            return response
        for ip in ip_dict.values():
            if not ipv4_re.match(ip):
                response.message = u"Ip地址格式错误"
                return response
        start_list = start_ip.split(".")
        end_list = end_ip.split(".")
        if start_list[0] != end_list[0] or start_list[1] != end_list[1] or start_list[2] != end_list[2]:
            response.message = u"IP地址段输入错误"
            return response
        diff = int(str(end_list[3])) - int(str(start_list[3]))
        print "diff", diff
        if diff < 0:
            response.message = u"IP地址段输入错误(注意IP地址顺序)"
            return response
        ip_list = []
        l = int(start_list[3])
        for i in range(diff + 1):
            start_list[3] = str(l+i)
            ip_list.append(".".join(start_list))
        re_list = ping_host_ip.run_ping_by_ip(ip_list)

        response.data = re_list
        response.status = True
        return response
    except Exception, e:
        response.message = str(e)
        return response


def file_ping(filename, up_dir):
    '''
    通过上传文件来ping
    '''

    response = BaseResponse()
    try:
        # 开始读取文件中的内容
        file_dir = up_dir + filename
        print "file_===================dir", file_dir
        is_have = os.path.isfile(file_dir)
        if not is_have:
            response.message = u'指定文件不存在'
            return response
        ip_list = read_ip_from_file(file_dir)
        print "ip_=================list", ip_list
        re_list = ping_host_ip.run_ping_by_ip(ip_list)
        response.data = re_list
        response.status = True
        return response

    except Exception, e:
        response.message = str(e)
        return response


def upload_ping_file(file_obj, filename, up_dir):
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


def read_ip_from_file(file_dir):
    '''
    读取一个文件中内容
    '''
    ip_list = []
    excel_obj = xlrd.open_workbook(file_dir)
    sheet = excel_obj.sheet_by_index(0)

    ip_lie = sheet.col_values(0)
    for ip in ip_lie:
        ip = ip.strip()
        if ipv4_re.match(ip):
            ip_list.append(ip)
    return ip_list


def get_ping_file(file_dir):
    '''
    获取所有的上传ping文件
    '''
    response = BaseResponse()

    try:
        file_list = []
        all_file_list = os.listdir(file_dir)
        for file_name in all_file_list:
            if file_name.endswith('xlsx'):
                file_list.append(file_name)          # 将正确格式的文件筛选出
        print "file_______________list", file_list

        response.data = file_list
        response.status = True
        return response

    except Exception, e:
        response.message = str(e)
        return response


def delete_ping_file(file_dir):
    '''
    删除所有的上传ping文件
    '''
    response = BaseResponse()

    try:
        all_file_list = os.listdir(file_dir)
        print ">>>>>>>>>>>>>>>>>>>>", all_file_list
        for file_name in all_file_list:
            print "<<<<<<<<<<<<<<<<<<<<<", file_dir+file_name
            os.remove(file_dir+file_name)
        # all_file_list2 = os.listdir(file_dir)
        response.status = True
        return response
    except Exception, e:
        response.message = str(e)
        return response




















