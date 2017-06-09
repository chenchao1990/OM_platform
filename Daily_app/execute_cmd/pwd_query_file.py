#!/usr/bin/env python
# _*_coding:utf-8 _*_

import hashlib
import json
import commands
import sys
import os


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


def data_json(md5_str, info_list, envir):
    data_dict = {
            "operater": "chenchao-ds",
            "sign": md5_str,
            "accounts": [],
            "envir": envir
        }
    for ip_list in info_list:
        data_dict["accounts"].append({"ip": ip_list[0], "user": ip_list[1]})
    json_dict = json.dumps(data_dict)

    return json_dict


def curl_post_cmd(json_dict):
    key_dir = os.path.dirname(os.path.abspath(__file__))
    w = '''curl -k -E  %s/keypasspc.pem -H "Content-Type: application/json" -d '%s' https://strongbox.cloud.api:8443/keypass/account/query > query_result''' % (key_dir, json_dict)
    rm_file = "rm -f %s/query_result" % key_dir

    (post_state, post_result) = commands.getstatusoutput(w)
    ret_dict = {}
    if post_state == 0:
        with open('query_result', 'r') as re_obj:
            for line in re_obj:
                ret_dict = json.loads(line)
        (re_state, re_result) = commands.getstatusoutput(rm_file)
        return ret_dict
    else:
        (re_state, re_result) = commands.getstatusoutput(rm_file)
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


def main(ip_list, info_list, envir_str):

    sort_str_re = sort_str(ip_list)
    user_key_re = user_key(sort_str_re)
    post_dict_json = data_json(user_key_re, info_list, envir_str)
    post_result = curl_post_cmd(post_dict_json)
    # result_dict = loads_dict(post_result)
    return post_result




