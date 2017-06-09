#!/usr/bin/env python
# -*- coding:utf-8 -*-
from multiprocessing import Pool
import commands

re_list = []


def join_result(array_result):
    lines = []
    for i in array_result:
        if i != "\n":
            lines.append(i)
        else:
            yield "".join(lines)
            lines = []


def action(ip):

    cmd = "ping -c 2 "

    (array_state, array_result) = commands.getstatusoutput(cmd + ip)        # run ping cmd + host_ip
    if array_state == 0 and array_result is not None:                       # the cmd is run OK
        for line in join_result(array_result + "\n"):
            if "packets transmitted" in line.strip():
                received = line.strip().split(",")[1].strip().split()[0]
                received = int(received)
                if received == 0:           # 说明不通  4个包都不可达
                    q = "%s: error" % ip
                else:
                    q = "%s: OK" % ip
                    r = {"state": "0", "re":q}
                    return r
    else:                                                                   # 命令运行失败
        for line in join_result(array_result + "\n"):
            if "packets transmitted" in line.strip():
                received = line.strip().split(",")[1].strip().split()[0]
                received = int(received)
                if received == 0:           # 说明不通  4个包都不可达
                    q = "%s: error" % ip
                    r = {"state": "1", "re": q}
                    return r
                else:
                    q = "%s: OK!" % ip


def collect_re(arg):
    re_list.append(arg)


def run_ping_by_ip(ip_list):
    if len(re_list) != 0:
        del re_list[:]
    pool = Pool(15)

    for ip in ip_list:
        pool.apply_async(func=action, args=(ip,), callback=collect_re)

    print 'end'
    pool.close()
    # pool.teminate()  # 结束工作进程，不在处理未完成的任务。
    pool.join() # 进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。
    return re_list
