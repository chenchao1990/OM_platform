#!/usr/bin/env python
# _*_coding:utf-8 _*_

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager

from ansible.plugins.callback import CallbackBase
import json


class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def __init__(self, *args):
        super(ResultCallback, self).__init__(display=None)
        self.status_ok = json.dumps({})
        self.status_fail = json.dumps({})
        self.status_unreachable = json.dumps({})
        self.status_playbook = ''
        self.status_no_hosts = False
        self.host_ok = []                   # 存放执行成功的数据
        self.host_failed = []               # 存放执行失败的数据
        self.host_unreachable = []          # 存放主机不能访问的数据

    def v2_runner_on_ok(self, result):
        host = result._host
        self.runner_on_ok(host, result._result)
        # res = json.dumps({host.name:result._result}, indent=4)
        # print "ansible run OK-------------", res
        re_data = None

        if result._result.get('stdout_lines', False):
            re_data = "<br>".join(result._result.get('stdout_lines'))
        elif result._result.get('checksum', False):
            re_data = "SUCCESS"
        self.host_ok.append({'ip': host.name, 'result': json.dumps(re_data)})

    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host
        self.runner_on_failed(host, result._result, ignore_errors)
        re_data = result._result.get('stderr', None)
        error_lines = result._result.get('stdout_lines', None)
        error_msg = result._result.get('msg', None)
        if re_data:
            self.host_failed.append({'ip': host.name, 'result': re_data})
        if error_msg:
            self.host_failed.append({'ip': host.name, 'result': error_msg})
        if error_lines:
            error_str = "/n".join(error_lines)
            self.host_failed.append({'ip': host.name, 'result': error_str})

    def v2_runner_on_unreachable(self, result):
        host = result._host
        self.runner_on_unreachable(host, result._result)
        re_data = result._result.get('msg')

        self.host_unreachable.append({'ip': host.name, 'result': re_data})


class Ansible_API(object):
    def __init__(self, host_list='/etc/ansible/hosts'):
        self.host = 'test'
        self.host_file = host_list
        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.inventory = Inventory(loader=self.loader, variable_manager=self.variable_manager,
                                   host_list=host_list)
        self.variable_manager.set_inventory(self.inventory)
        self.passwords = {}
        self.results_callback = ResultCallback()
        Options = namedtuple('Options',
                         ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection', 'module_path',
                          'forks', 'private_key_file', 'ssh_common_args', 'ssh_extra_args',
                          'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check']
                         )

        self.options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh',
                              module_path=None, forks=50, private_key_file=None, ssh_common_args=None,
                              ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=False,
                              become_method=None, become_user=None, verbosity=None, check=False)

    def receive_source_run(self, source_dict):
        play = Play().load(source_dict, variable_manager=self.variable_manager, loader=self.loader)
        tqm = None
        try:
            tqm = TaskQueueManager(
                  inventory=self.inventory,
                  variable_manager=self.variable_manager,
                  loader=self.loader,
                  options=self.options,
                  passwords=self.passwords,
                  stdout_callback=self.results_callback,
                  )
            tqm.run(play)

        finally:
            if tqm is not None:
                tqm.cleanup()
            re = self.result_count()
            return re

    def shell_run(self, cmd_str):
        print "ansible _cmd  ", cmd_str,type(cmd_str)
        # cmd_str = cmd_str[0]
        play_source = dict(
                name="Ansible Shell",
                hosts=self.host,
                gather_facts='no',
                tasks=[
                    dict(action=dict(module='shell', args=cmd_str))
                 ]
          )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        tqm = None
        try:
            tqm = TaskQueueManager(
                  inventory=self.inventory,
                  variable_manager=self.variable_manager,
                  loader=self.loader,
                  options=self.options,
                  passwords=self.passwords,
                  stdout_callback=self.results_callback,
                  )
            tqm.run(play)
        except Exception, e:
            print "shell_run Error: "
        finally:
            if tqm is not None:
                tqm.cleanup()
            re = self.result_count()
            return re

    def run_script(self, script_path):      # 执行脚本API
        source_dict = dict(
                name="run script",
                hosts=self.host,
                gather_facts='no',
                tasks=[
                    dict(action=dict(module='script', args=script_path))
                 ]
          )
        print "self.host", self.host
        run_result = self.receive_source_run(source_dict)
        return run_result

    def send_file(self, filename):
        play_source = dict(
                name="Ansible Shell",
                hosts=self.host,
                gather_facts='no',
                tasks=[
                    dict(action=dict(module='copy', args="src=/ansible_tmp/%s dest=/tmp/" % filename.encode('utf8')))
                 ]
          )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        tqm = None
        try:
            tqm = TaskQueueManager(
                  inventory=self.inventory,
                  variable_manager=self.variable_manager,
                  loader=self.loader,
                  options=self.options,
                  passwords=self.passwords,
                  stdout_callback=self.results_callback,
                  )
            tqm.run(play)

        finally:
            if tqm is not None:
                tqm.cleanup()
            re = self.result_count()
            return re

    def result_count(self):

        all_times = len(self.results_callback.host_ok) + len(self.results_callback.host_failed) + len(self.results_callback.host_unreachable)
        ok_times = len(self.results_callback.host_ok)
        error_times = len(self.results_callback.host_failed)
        unkown_times = len(self.results_callback.host_unreachable)
        msg = u'共执行 %s次， 成功 %s次， 失败 %s次， 主机连接失败 %s次' %  (all_times, ok_times, error_times, unkown_times)
        result_dict = {'all_times': all_times,
                       'result_msg': msg,
                       'run_ok': self.results_callback.host_ok,
                       'ok_times': ok_times,
                       'run_failed': self.results_callback.host_failed,
                       'error_times': error_times,
                       'host_unreachable': self.results_callback.host_unreachable,
                       'unkown_times': unkown_times}
        return result_dict

