#!/usr/bin/env python
# _*_coding:utf-8 _*_

from overall.response.base_response import BaseResponse


def create_host_file(host_list):
    '''
    制作一个全新的host  在/etc/ansible/hosts
    :param host_list:
    :return:
    '''
    host_url = '/etc/ansible/hosts'
    with open(host_url, 'w') as file_obj:
        file_obj.write('[test]' + '\n')
        for host_dict in host_list:
            ip = host_dict['ip']
            pwd = host_dict['pwd']
            user = host_dict['user']
            hosts_info = ip + ' ' + 'ansible_ssh_pass=' + "'%s'" % pwd + ' ' + 'ansible_ssh_user=' + "'%s'" % user+'\n'
            file_obj.write(hosts_info)
    print "create____host___file_____OK~~~~"
    return


def create_iptables_host_file(host_list):
    '''
    制作一个全新的iptables host file  在/etc/ansible/iptables_host
    :param host_list:
    :return:
    '''
    host_url = '/etc/ansible/iptables_host'
    response = BaseResponse()
    try:
        with open(host_url, 'w') as file_obj:
            file_obj.write('[iptables]' + '\n')
            for host_dict in host_list:
                ip = host_dict['ip']
                pwd = host_dict['pwd']
                user = host_dict['user']
                hosts_info = ip + ' ' + 'ansible_ssh_pass=' + "'%s'" % pwd + ' ' + 'ansible_ssh_user=' + "'%s'" % user+'\n'
                file_obj.write(hosts_info)
        print "create____host___file_____OK~~~~"
        response.status = True
        response.data = host_url
    except Exception, e:
        print "create_iptables_host_file Error: ", e
        response.message = str(e)
    return response


def create_ansible_host_file(host_list, hostname):
    '''
    制作一个全新的iptables host file  在/etc/ansible/iptables_host
    :param host_list:
    :return:
    '''
    host_url = '/etc/ansible/%s' % hostname
    response = BaseResponse()
    try:
        with open(host_url, 'w') as file_obj:
            file_obj.write('[%s]' % hostname + '\n')
            for host_dict in host_list:
                ip = host_dict['ip']
                pwd = host_dict['pwd']
                user = host_dict['user']
                hosts_info = ip + ' ' + 'ansible_ssh_pass=' + "'%s'" % pwd + ' ' + 'ansible_ssh_user=' + "'%s'" % user +'\n'
                file_obj.write(hosts_info)
        print "create____host___file_____OK~~~~"
        response.status = True
        response.data = host_url
    except Exception, e:
        print "create_iptables_host_file Error: ", e
        response.message = str(e)
    return response
