#!/usr/bin/env python
# _*_coding:utf-8 _*_

import paramiko
import re


class RunIptables(object):
    def __init__(self, iptables_list, host, password):
        self.username = "root"
        self.port = 22
        self.password = password
        self.iptables_list = iptables_list
        self.host = host

    def line_generator(self, result_str):
        line = []
        for c in result_str:
            if c != '\n':
                line.append(c)
            else:
                yield ''.join(line)
                line = []

    def connect(self):
        '''
        通用的方式连接服务器
        '''
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        self.transport = transport

    def execute_iptables(self):
        '''
        在远程主机上执行iptables 命令
        '''
        self.run()
        try:
            ssh = paramiko.SSHClient()
            ssh._transport = self.transport
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            for rule_str in self.iptables_list:                     # 循环  执行所有的iptables命令
                stdin, stdout, stderr = ssh.exec_command(rule_str)
                stdout.read()
                stderr.read()

            stdin, stdout, stderr = ssh.exec_command("service iptables save")       # 重启iptables服务 使变更生效
            runout = stdout.read()
            errout = stderr.read()
            re_dict = {}
            if runout:
                re_dict["ip"] = self.host
                re_dict["msg"] = ":  OK!"
                re_dict["state"] = 0
            elif errout:
                re_dict["ip"] = self.host
                re_dict["msg"] = ":  ERROR!"
                re_dict["state"] = 1
            return re_dict
        except Exception, e:                        # 将上传失败的错误返回
            return str(e)
        finally:
            self.close()

    def re_ip(self, ip, line_str):
        if ip in line_str:
            re_list = line_str.split("INPUT")[1].strip().split("-j")[0].strip().split()[1].split("/")
            if ip == re_list[0]:
                return True

    def re_other(self, essence, line_str):
        if essence in line_str:
            re_list = line_str.split("INPUT")[1].strip().split("-j")[0].strip()
            if re_list == essence:
                return True

    def get_all_rules(self):
        '''
        获取主机下所有的规则
        :return:
        '''
        self.run()

        check_result_dict = {}
        rule_list = []
        try:
            ssh2 = paramiko.SSHClient()
            ssh2._transport = self.transport
            ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            stdin, stdout, stderr = ssh2.exec_command("cat /etc/sysconfig/iptables")
            runout = stdout.read()
            runerr = stderr.read()
            if runout:
                for line in self.line_generator(runout):
                    if line.startswith("#"):
                        pass
                    elif line.startswith(":"):
                        pass
                    elif line.startswith("*"):
                        pass
                    elif line.startswith("COMMIT"):
                        pass
                    else:
                        rule_list.append(line.strip())
            check_result_dict['ip'] = self.host
            check_result_dict['rules'] = rule_list
            return check_result_dict
        except Exception, e:
            return str(e)
        finally:
            self.close()

    def checkout_iptables_rule(self, check_ip):
        '''
        检查iptables配置文件中是否有此规则
        '''
        print "22222222222222222"
        self.run()
        check_result_dict = {}
        have_list = []
        try:
            ssh2 = paramiko.SSHClient()
            ssh2._transport = self.transport
            ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print "3333333333333333333"
            stdin, stdout, stderr = ssh2.exec_command("cat /etc/sysconfig/iptables")

            runout = stdout.read()
            runerr = stderr.read()

            if runout:
                for line in self.line_generator(runout):        # 遍历iptables配置文件内容
                    for ip in check_ip:                         # 判断检查的IP 是否在配置文件中
                        # if ip in line.strip():
                        re_result =self.re_ip(ip, line.strip())
                        if re_result:
                            have_list.append(line.strip())      # 如果在 将整条配置添加到列表中
                    for rule in self.iptables_list:
                        essence = rule.split("INPUT")[1].strip().split("-j")[0].strip()

                        re_result =self.re_other(essence, line.strip())
                        if re_result:
                            have_list.append(line.strip())

            return have_list
        except Exception, e:
            return str(e)
        finally:
            self.close()

    def close(self):
        self.transport.close()

    def run(self):
        try:
            self.connect()
        except Exception, e:
            return str(e)                           # 将连接失败的错误返回

