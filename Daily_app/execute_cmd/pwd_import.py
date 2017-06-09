#!/usr/bin/env python
# _*_coding:utf-8 _*_

import hashlib
import json
import commands
import sys
import re
import os

key_dir = os.path.dirname(os.path.abspath(__file__))


def sort_str(ip_list):
    arg = ["chenchao-ds", "201681157030962403332"]
    for ip in ip_list:
        arg.append(ip.strip())
    up_sort = sorted(arg)
    data_str = "&".join(up_sort) + "54ea77d9005590a9"

    return data_str


def user_key(data_str):
    hash_obj = hashlib.md5()
    hash_obj.update(data_str)
    md5_str = hash_obj.hexdigest()
    return md5_str


def read_file():
    data_list = []
    all_ip_list = []
    with open('password.txt', 'r') as file_obj:
        for line in file_obj:
            split_span_list = []
            line_list =line.strip().split("\t")           # 这是从文件中读取的没一行数据 为一个列表
            if len(line_list) >2:
                ip_addr = line_list[0].strip()
                all_ip_list.append(ip_addr)             # 将IP地址添加到列表
                split_span_list.append(ip_addr)         # 将IP添加
                user = line_list[1].strip()
                pwd = line_list[2]
                new_pwd = re.sub("\'", '*', pwd)        # 将密码中的'符号 替换为* 避免curl命令的失败
                #new_pwd = re.sub("\,", '*', new_pwd)        # 将密码中的'符号 替换为* 避免curl命令的失败
                split_span_list.append(user)          # 将文件中的用户添加到小列表
                split_span_list.append(new_pwd)         # 将密码添加到小列表
                data_list.append(split_span_list)           # 将小列表 添加到大列表 并返回

    return all_ip_list, data_list


def query_data_json(md5_str, data_list, environment):
    '''
    查询密码的json dict
    '''
    data_dict = {
            "operater": "chenchao-ds",
            "sign": md5_str,
            "accounts": [],
            "envir": environment
        }
    for user_list in data_list:
        data_dict["accounts"].append({"ip": user_list[0].strip(), "user": user_list[1].strip()})
    json_dict = json.dumps(data_dict)

    return json_dict


def data_json(md5_str, ip_list, environment):
    data_dict = {
            "operater": "chenchao-ds",
            "sign": md5_str,
            "accounts": [],
        }
    for ip in ip_list:
        data_dict["accounts"].append({"ip": ip[0], "user": ip[1], "pwd": ip[2], "envir": environment})
    json_dict = json.dumps(data_dict)

    return json_dict


def update_data_json(md5_str, ip_data_list, environment):
    data_dict = {
            "operater": "chenchao-ds",
            "sign": md5_str,
            "accounts": [],
        }

    for ip in ip_data_list:
        data_dict["accounts"].append({"ip": ip[0], "user": ip[1], "pwd": ip[2], "envir": environment, "del": "N"})
    json_dict = json.dumps(data_dict)

    return json_dict


def query_curl_cmd(json_dict):
    '''
    查询密码
    '''
    w = '''curl -k -E  %s/keypasspc.pem -H "Content-Type: application/json" -d '%s'   https://strongbox.cloud.api:8443/keypass/account/query''' % (key_dir, json_dict)
    (post_state, post_result) = commands.getstatusoutput(w)
    if post_state == 0:
        return post_result
    else:
        sys.exit("query curl cmd is Error!!!!")


def curl_post_cmd(json_dict):
    w = '''curl -k -E  %s/keypasspc.pem -H "Content-Type: application/json" -d '%s'   https://strongbox.cloud.api:8443/keypass/account/save''' % (key_dir, json_dict)
    (post_state, post_result) = commands.getstatusoutput(w)

    if post_state == 0:
        return post_result
    else:
        sys.exit("curl cmd is Error!!!!")


def update_curl_cmd(json_dict):
    w = '''curl -k -E  %s/keypasspc.pem -H "Content-Type: application/json" -d '%s' https://strongbox.cloud.api:8443/keypass/account/update''' % (key_dir, json_dict)
    w = '''curl -k -E  %s/keypasspc.pem -H "Content-Type: application/json" -d '%s' https://strongbox.cloud.api:8443/keypass/account/update''' % (key_dir, json_dict)
    (post_state, post_result) = commands.getstatusoutput(w)

    if post_state == 0:
        return post_result
    else:
        sys.exit("curl cmd is Error!!!!")


def line_generator(string):
    line = []
    for c in string:
        if c != '\n':
            line.append(c)
        else:
            yield ''.join(line)
            line = []


def loads_dict(post_result):
    for line in line_generator(post_result + "\n"):
        if "status" in line:
            result_dict = json.loads(line)
            return result_dict


def query_achieve_result(result_dict):
    '''
    将查找到的IP取出 存到列表中返回
    '''
    is_have_list = []
    if result_dict["status"] == "success":
        data_list = result_dict["result"]
        for dict_value in data_list:
            is_have_list.append(dict_value["ip"])           # 将IP查找到的IP取出
    return is_have_list


def achieve_result(result_dict):
    if result_dict["status"] == "success":
        return True, None
    else:
        return False, result_dict["message"]


def main(all_ip_list, data_list, envir_str):
    try:
        re_dict = {'import_re': False, 'message': ''}
        sort_string = sort_str(all_ip_list)                    # 生成排序后的字符串 请求数据
        md5_user_key = user_key(sort_string)                   # 生成请求数据的MD5值

        query_data = query_data_json(md5_user_key, data_list, envir_str)        # 先将所有的IP查询一遍
        query_result = query_curl_cmd(query_data)                               # 查询的结果
        query_result_dict = loads_dict(query_result)                            # 将查询的结果筛选
        is_have_ip_list = query_achieve_result(query_result_dict)               # 已存在的IP列表
        # 基于以存在IP的列表，将原所有IP列表进行筛选，使其只剩下不存在的IP列表
        new_all_ip_list = []                # 密码库里不存在的IP
        new_data_list = []
        is_have_date_list = []
        if len(is_have_ip_list) > 0:                    # 如果已存在IP的列表不为空 说明有IP已经在库里 需要筛选
            for is_ip in all_ip_list:
                if is_ip not in is_have_ip_list:
                    not_have_ip = all_ip_list[all_ip_list.index(is_ip)]
                    new_all_ip_list.append(not_have_ip)                                  # 将不存在的ip添加到新列表中

            for ip_list in data_list:
                ip = ip_list[0].strip()
                if ip not in is_have_ip_list:
                    new_data_list.append(ip_list)                           # 同样将不存在的IP列表 添加到新列表中
                else:
                    is_have_date_list.append(ip_list)                       # 将存在的IP 归为一类

        else:                                           # 如果已存在IP为空 说明都是新的数据 直接写入库即可
            '''
            直接保存 新的IP密码
            '''
            old_dict_json = data_json(md5_user_key, data_list, envir_str)
            old_post_result = curl_post_cmd(old_dict_json)
            old_result_dict = loads_dict(old_post_result)
            save_re, error_msg = achieve_result(old_result_dict)
            if save_re:
                re_dict['import_re'] = True
            else:
                re_dict['import_re'] = False
                re_dict['message'] = error_msg
                return re_dict

        # 基于新生成的IP数据列表，将密码导入到库中
        if len(new_data_list) > 0:                              # 当过滤后的新列表不为空时
            sort_string2 = sort_str(new_all_ip_list)                            # 将新生成的列表在排序
            md5_user_key2 = user_key(sort_string2)                              # 生成请求数据的MD5值

            post_dict_json = data_json(md5_user_key2, new_data_list, envir_str)          # 将所有数据生成一个json的字典
            post_result = curl_post_cmd(post_dict_json)                         # 将数据封装后 提交申请
            result_dict = loads_dict(post_result)
            save_new_re, error_msg = achieve_result(result_dict)
            if save_new_re:
                re_dict['import_re'] = True
            else:
                re_dict['import_re'] = False
                re_dict['message'] = error_msg
                return re_dict
            # 将已经存在的IP 进行密码更新
        if len(is_have_date_list) > 0:
            update_sort_str = sort_str(is_have_ip_list)
            update_md5_key = user_key(update_sort_str)
            update_dict_json = update_data_json(update_md5_key, is_have_date_list, envir_str)
            update_result = update_curl_cmd(update_dict_json)
            update_result_dict = loads_dict(update_result)
            update_re, error_msg = achieve_result(update_result_dict)
            if update_re:
                re_dict['import_re'] = True
            else:
                re_dict['import_re'] = False
                re_dict['message'] = error_msg
                return re_dict
        return re_dict
    except Exception, e:
        print str(e)
