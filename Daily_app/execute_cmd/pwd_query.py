#!/usr/bin/env python
# _*_coding:utf-8 _*_

import hashlib
import json
import commands
import sys
import datetime
import os
import re


def sort_str(ip_list):
    print "IP_____________list", ip_list
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


def data_json(md5_str, info_list, ip_list, envir, is_win=False, special_user=None):

    data_dict = {
            "operater": "chenchao-ds",
            "sign": md5_str,
            "accounts": [],
            "envir": envir
        }
    print "ssssssssssssssssssssss___user", special_user
    print "is___win", is_win
    if special_user:
        user = special_user
    else:
        user = "root"
    if len(info_list) == 0:                 # 说明只是输入的IP地址
        for ip in ip_list:
            if is_win:
                print "IIIIIIIIIIIIIIIIIIIIIIIIIS win"
                if special_user:
                    data_dict["accounts"].append({"ip": ip.strip(), "user": user})
                else:
                    data_dict["accounts"].append({"ip": ip.strip(), "user": user})
                    data_dict["accounts"].append({"ip": ip.strip(), "user": "administrator"})
            else:
                print "TTTTTTTTTTTTTTTTThis is no admin checked"
                data_dict["accounts"].append({"ip": ip.strip(), "user": user})
    else:
        for ip_data_list in info_list:
            data_dict["accounts"].append({"ip": ip_data_list[0].strip(), "user": ip_data_list[1]})
    json_dict = json.dumps(data_dict)

    return json_dict


def curl_post_cmd(json_dict):
    key_dir = os.path.dirname(os.path.abspath(__file__))
    w = '''curl -k -E  %s/keypasspc.pem -H "Content-Type: application/json" -d '%s'   https://10.58.188.92:8443/keypass/account/query > query_result''' % (key_dir, json_dict)
    # w = '''curl -k -E  %s/certificate_alias_client.pem -H "Content-Type: application/json" -d '%s' https://strongbox.cloud.api:8443/keypass/account/query > query_result ''' % (key_dir, json_dict)
    print "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww", w
    rm_file = "rm -f query_result"

    (post_state, post_result) = commands.getstatusoutput(w)
    print "CURL commands result: ", post_result
    ret_dict = {}
    if post_state == 0:
        with open('query_result', 'r') as re_obj:
            for line in re_obj:
                ret_dict = json.loads(line)
        (re_state, re_result) = commands.getstatusoutput(rm_file)
        # return post_result
        return ret_dict
    else:
        # (re_state, re_result) = commands.getstatusoutput(rm_file)
        sys.exit("curl cmd is Error!!!!")


def line_generator(string):
    line = []
    for c in string:
        if c != '\n':
            line.append(c)
        else:
            yield ''.join(line)
            line = []


# def loads_dict(post_result):
#     print "post____result", post_result, type(post_result)
#     # for line in line_generator(post_result + "\n"):
#     #     if "status" in line:
#     if post_result['']
#             result_dict = json.loads(line)
#             return result_dict


def achieve_result(result_dict):
    print "check_result", result_dict
    if result_dict["status"] == "success":
        data_list = result_dict["result"]
        return data_list
    else:

        pass


def post_data(ip_list, info_list, envir_str, is_win=False, special_user=None):
    if is_win:
        if not special_user:
            win_ip_list = [i for i in ip_list]
            win_ip_list.extend(win_ip_list)
        else:
            win_ip_list = ip_list
        sort_dict = sort_str(win_ip_list)
        user_key_str = user_key(sort_dict)
        post_dict_json = data_json(user_key_str, info_list, ip_list, envir_str, is_win, special_user)
        post_result = curl_post_cmd(post_dict_json)
        re_list = achieve_result(post_result)
        return re_list
    else:
        sort_dict = sort_str(ip_list)
        user_key_str = user_key(sort_dict)
        post_dict_json = data_json(user_key_str, info_list, ip_list, envir_str, special_user=special_user)
        post_result = curl_post_cmd(post_dict_json)
        re_list = achieve_result(post_result)
        return re_list


def main(ip_list, ip_info_list,  envir_str, is_win=False, special_user=None):

    # re_list = []
    # len_ip = len(ip_list)
    # post_times_tuple = divmod(len_ip, 50)
    # print "ip___list", ip_list, type(ip_list), len(ip_list)
    # print "ip_info_list", ip_info_list, type(ip_info_list), len(ip_info_list)
    # print "1111111111111111111111111111"
    # i = 0
    # for num in range(post_times_tuple[0]):
    #
    #     once_time_re = post_data(ip_list[i: i+40], ip_info_list[i: i+50], envir_str)
    #     print "22222222222222222222222222222"
    #     re_list.extend(once_time_re)
    #     i += 40
    # print "33333333333333333333333333333"
    # surplus_re_list = post_data(ip_list[i:], ip_info_list, envir_str)

    strip_ip = []
    for ip in ip_list:
        strip_ip.append(ip.strip())
    re_list = post_data(strip_ip, ip_info_list, envir_str, is_win, special_user)
    # print "4444444444444444444444444444"
    # re_list.extend(surplus_re_list)

    return re_list





