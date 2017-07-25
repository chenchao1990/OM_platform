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


def set_user_pwd(host_ip, username, old_pwd, new_pwd, name):
    re_dict = {'ip': host_ip, 'status': None, 'queue_name': name}
    try:
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname=host_ip, port=22, username="root", password=old_pwd, timeout=5)
    except Exception, e:
        re_dict['status'] = 'connect error'
        return re_dict

    '''
    先利用旧密码登录服务器 发送修改密码命令修改为新密码
    '''
    change_cmd = "echo '%r' | passwd --stdin root" % new_pwd
    stdin, stdout, stderr = s.exec_command(change_cmd)
    change_out = stdout.read()
    change_err = stderr.read()
    if change_out:
        print "ssssssssssssssssssssssssssssss", change_out
        re_dict['status'] = "successful"
    if change_err:
        print "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", change_err
        re_dict['status'] = "error"

    return re_dict


def set_pwd(host_ip, username, old_pwd, new_pwd, name):
    re_dict = {'ip': host_ip, 'status': None, 'queue_name': name}
    try:
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname=host_ip, port=22, username="root", password=old_pwd, timeout=5)
    except Exception, e:
        re_dict['status'] = 'connect error'
        return re_dict


    '''
    先利用旧密码登录服务器 发送修改密码命令修改为新密码
    '''
    change_cmd = "passwd"
    ssh = s.invoke_shell()
    time.sleep(0.1)
    ssh.send(change_cmd + '\n')                 # 执行修改密码命令
    buff = ''
    while not buff.endswith('password: '):
        resp = ssh.recv(9999)
        buff += resp
        print "000000000000000000000", buff
    print "11111111111111111111", buff
    ssh.send(new_pwd + '\n')                           # 第一次输入密码
    buff = ''
    while not buff.endswith('password: '):
        resp = ssh.recv(9999)
        buff += resp
    print "22222222222222222222222222", buff
    ssh.send(new_pwd + "\n")                           # 第二次输入密码
    buff = ''
    while not buff.endswith('# '):
        resp = ssh.recv(9999)
        buff += resp
    print "333333333333333333333333", buff
    s.close()
    for line in line_generator(buff):
        if "successful" in line.strip():
            re_dict['status'] = 'successful'
            return re_dict


def collect_re(arg):
    print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", arg
    name = arg.pop('queue_name')
    q = RedisQueue.RedisQueue(name)
    q.put(arg)
    re_list.append(arg)


def change_host_pwd(data_list):
    del re_list[:]
    pool = Pool(15)
    name = RedisQueue.queue_id()
    for value_list in data_list:
        ip = value_list[0]
        username = value_list[1]
        old_pwd = value_list[2]
        new_pwd = value_list[3]
        pool.apply_async(func=set_user_pwd, args=(ip, username, old_pwd, new_pwd, name), callback=collect_re)
        # pool.apply_async(func=set_user_pwd, args=(ip, username, old_pwd, new_pwd, name))

    pool.close()
    pool.join()     # 进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。
    return re_list, name
