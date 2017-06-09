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
        self.status_ok=json.dumps({})
        self.status_fail=json.dumps({})
        self.status_unreachable=json.dumps({})
        self.status_playbook=''
        self.status_no_hosts=False
        self.host_ok = []
        self.host_failed={}
        self.host_unreachable={}

    def v2_runner_on_ok(self,result):
        host=result._host
        self.runner_on_ok(host, result._result)
        res = json.dumps({host.name:result._result},indent=4)
        self.host_ok.append(res)


results_callback = ResultCallback()


class TaskRun(object):
    def __init__(self):
        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.inventory = Inventory(loader=self.loader, variable_manager=self.variable_manager)
        self.variable_manager.set_inventory(self.inventory)
        self.passwords = {}
        Options = namedtuple('Options',
                         ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection','module_path',
                          'forks', 'private_key_file', 'ssh_common_args', 'ssh_extra_args',
                          'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check']
                         )

        self.options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh',
                      module_path=None, forks=20, private_key_file=None,ssh_common_args=None,
                      ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=False,
                      become_method=None, become_user=None, verbosity=None, check=False)


        self.play_source = dict(
                name = "Ansible Play",
                hosts = ['10.58.56.211','10.58.56.202'],
                gather_facts = 'no',
                tasks = [
                    dict(action=dict(module='shell', args='ifconfig'))
                 ]
          )

    def shell_run(self):
        play = Play().load(self.play_source, variable_manager=self.variable_manager, loader=self.loader)
        tqm = None
        try:
            tqm = TaskQueueManager(
                      inventory=self.inventory,
                      variable_manager=self.variable_manager,
                      loader=self.loader,
                      options=self.options,
                      passwords=self.passwords,
                      stdout_callback=results_callback,
                  )
            tqm.run(play)

        finally:
            if tqm is not None:
                tqm.cleanup()
            return results_callback.host_ok
if  __name__ == '__main__':
    w = TaskRun()
    result = w.shell_run()
    for i in result:
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", i