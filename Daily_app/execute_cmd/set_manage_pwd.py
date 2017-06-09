#!/usr/bin/env python
# _*_coding:utf-8 _*_

from multiprocessing import Pool
import time
import commands

StopEvent = object()

re_list = []


def line_generator(result_str):
    line = []
    for c in result_str:
        if c != '\n':
            line.append(c)
        else:
            yield ''.join(line)
            line = []


def set_pwd(host_ip, username, old_pwd, new_pwd):
    re_dict = {'ip': host_ip, 'status': None, 'msg':''}
    change_cmd = "ipmitool -I lanplus -H %s  -U %s  -P %s user set password 1 %s" % (host_ip, username, old_pwd, new_pwd)
    run_state, run_result = commands.getstatusoutput(change_cmd)
    if run_state == 0:
        print "ooooooooookkkkkkkkkk", run_result
        re_dict['status'] = "Success."
    else:
        print "eeeeeeeeeeeeeeeeeeee", run_result
        re_dict['status'] = "Faild."
        re_dict['msg'] = str(run_result)
    return re_dict


def collect_re(arg):
    re_list.append(arg)


def change_manage_pwd(data_list):
    del re_list[:]
    pool = Pool(8)
    for value_list in data_list:
        ip = value_list[0].strip()
        username = value_list[1].strip()
        old_pwd = value_list[2].strip()
        new_pwd = value_list[3].strip()
        pool.apply_async(func=set_pwd, args=(ip, username, old_pwd, new_pwd), callback=collect_re)

    pool.close()
    pool.join()     # 进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。
    return re_list
