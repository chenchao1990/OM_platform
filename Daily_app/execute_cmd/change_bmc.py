#!/usr/bin/env python
# _*_coding:utf-8 _*_

import subprocess
from multiprocessing import Pool


class ManageBMC(object):
    '''
    管理BMC的各种功能
    '''
    def __init__(self, host_list):
        self.host_list = host_list
        self.change_re = []
        print "1111111111111111111", host_list

    # def task_pool(self, task, args_list):
    #     '''
    #     存放任务的进程池
    #     '''
    #
    #     arg_count = len(args_list)
    #     l = []
    #     for i in range(arg_count):
    #         l.append(args_list[i])
    #     args_tuple = tuple(l)
    #     print "33333333333333333333", args_tuple
    #     # self._pool.apply_async(func=task, args=args_tuple, callback=self.collect_re)
    #     self._pool.apply_async(func=self.run_task, args=(task, args_tuple), callback=self.collect_re)

    def collect_re(self, arg):
        self.change_re.append(arg)

    def change_bmc_pwd(self, host_ip, user, old_pwd, new_pwd):
        '''
        修改BMC管理口的密码
        :return:
        '''
        cmd_str = "ipmitool -I lanplus -H %s  -U %s  -P %s user set password 1 %s" % (host_ip, user, old_pwd, new_pwd)
        ret = subprocess.call(cmd_str, shell=True)
        re_dict = {'host_ip': host_ip}
        if ret == 0:        # 执行成功
            re_dict['result'] = "success"

        elif ret == 1:
            re_dict['result'] = "failed"
        return re_dict

    def run_change_pwd(self):
        self._pool = Pool(15)
        for args_list in self.host_list:
            # self.task_pool(self.change_bmc_pwd, args_list)
            arg_count = len(args_list)
            l = []
            for i in range(arg_count):
                l.append(args_list[i])
            args_tuple = tuple(l)
            self._pool.apply_async(func=self.change_bmc_pwd, args=args_tuple, callback=self.collect_re)
        self._pool.close()
        self._pool.join()

        return self.change_re

change_re = []


def collect_re(arg):
    change_re.append(arg)


def run_change_cmd(host_ip, user, old_pwd, new_pwd):
    cmd_str = "ipmitool -I lanplus -H %s  -U %s  -P %s user set password 2 %s" % (host_ip, user, old_pwd, new_pwd)
    ret = subprocess.call(cmd_str, shell=True)
    re_dict = {'host_ip': host_ip}
    if ret == 0:        # 执行成功
        re_dict['result'] = "success"

    elif ret == 1:
        re_dict['result'] = "failed"
    return re_dict


def change_bmc_password(host_list):
    if len(change_re) != 0:
        del change_re[:]
    _pool = Pool(15)
    for args_list in host_list:
        arg_count = len(args_list)
        l = []
        for i in range(arg_count):
            l.append(args_list[i])
        args_tuple = tuple(l)
        _pool.apply_async(func=run_change_cmd, args=args_tuple, callback=collect_re)
    _pool.close()
    _pool.join()
    return change_re


