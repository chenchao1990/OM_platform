#!/usr/bin/env python
# _*_coding:utf-8 _*_

from multiprocessing import Pool
from overall.Task_Queue import RedisQueue
import time
import paramiko

re_list = []


def line_generator(result_str):
    line = []
    for c in result_str:
        if c != '\n':
            line.append(c)
        else:
            yield ''.join(line)
            line = []


def set_pwd(host_ip, username, old_pwd, new_pwd, name):
    re_dict = {'ip': host_ip, 'status': None}
    print "3333333333333333333333333333", re_dict
    try:
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname=host_ip, port=22, username="root", password=old_pwd, timeout=5)
    except Exception, e:
        re_dict['status'] = 'connect error'
        return re_dict, name


    '''
    先利用旧密码登录服务器 发送修改密码命令修改为新密码
    '''
    change_cmd = "passwd"
    ssh = s.invoke_shell()
    time.sleep(0.1)
    ssh.send(change_cmd + '\n')                 # 执行修改密码命令
    ssh.send('\n')

    buff = ''
    while not buff.endswith('password: '):
        resp = ssh.recv(9999)
        buff += resp
    ssh.send(new_pwd)                           # 第一次输入密码
    ssh.send('\n')                              # 回车确定
    buff = ''
    while not buff.endswith('password: '):
        resp = ssh.recv(9999)
        buff += resp
    ssh.send(new_pwd)                           # 第二次输入密码
    ssh.send("\n")
    buff = ''
    while not buff.endswith('# '):
        resp = ssh.recv(9999)
        buff += resp
    s.close()
    print "ccccccccccccccccccccccolse"
    print "bbbbbbbbbbbbbbbbbbbbbbbbb", buff
    for line in line_generator(buff):
        print "line--------", line
        if "successful" in line.strip():
            re_dict['status'] = 'successful'
            print "444444444444444444-2222", re_dict
        return re_dict, name


def collect_re(self, args):
    print "aaaaaaaaaaaargs", args
    arg = args[0]
    name = args[1]
    q = RedisQueue.RedisQueue(name)
    q.put(arg)
    print "argggggggggggggggggggggggg", arg
    re_list.append(arg)

    print "55555555555555555555555555555555"


def task_run(work_obj, host_ip, username, old_pwd, new_pwd):
    work_obj(host_ip, username, old_pwd, new_pwd)


class ChangePassword(object):

    def __init__(self, func):
        self.re_list = []
        self.name = RedisQueue.queue_id()
        self.set_pwd = func

    def change_host_pwd(self, data_list):
        print "data_________list", data_list
        del self.re_list[:]
        pool = Pool(15)
        print "1111111111111111111111"
        for value_list in data_list:
            ip = value_list[0]
            username = value_list[1]
            old_pwd = value_list[2]
            new_pwd = value_list[3]
            print "22222222222222222222"
            ret = pool.apply_async(func=self.set_pwd, args=(ip, username, old_pwd, new_pwd, self.name), callback=collect_re)
            print "rrrrrrrrrrrrrrrrrrrrrrrrrrrrr", ret.get()

        pool.close()
        pool.join()     # 进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。
        return self.re_list

