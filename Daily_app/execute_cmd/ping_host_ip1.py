#!/usr/bin/env python
# _*_coding:utf-8 _*_

import commands
import Queue
import threading
import contextlib

StopEvent = object()
task_queue = Queue.Queue()


class ThreadPool(object):

    def __init__(self, max_num, max_task_num = None):
        if max_task_num:
            self.q = Queue.Queue(max_task_num)
        else:
            self.q = Queue.Queue()
        self.max_num = max_num
        self.cancel = False
        self.terminal = False
        self.generate_list = []
        self.free_list = []

    def run(self, func, args, callback=None):

        if self.cancel:
            return
        if len(self.free_list) == 0 and len(self.generate_list) < self.max_num:
            self.generate_thread()
        w = (func, args, callback,)
        self.q.put(w)
    def generate_thread(self):

        t = threading.Thread(target=self.call)
        t.start()

    def call(self):
        current_thread = threading.currentThread
        self.generate_list.append(current_thread)

        event = self.q.get()
        while event != StopEvent:
            func, arguments, callback = event
            try:
                result = func(*arguments)           # 处理执行命令返回的结果
                success = True
            except Exception as e:
                success = False
                result = None

            if callback is not None:
                try:
                    callback(success, result)
                except Exception as e:
                    pass

            with self.worker_state(self.free_list, current_thread):
                if self.terminal:
                    event = StopEvent
                else:
                    event = self.q.get()
        else:

            self.generate_list.remove(current_thread)

    def close(self):
        self.cancel = True
        full_size = len(self.generate_list)
        while full_size:
            self.q.put(StopEvent)
            full_size -= 1

    def terminate(self):
        self.terminal = True
        while self.generate_list:
            self.q.put(StopEvent)

        self.q.empty()

    @contextlib.contextmanager
    def worker_state(self, state_list, worker_thread):
        state_list.append(worker_thread)
        try:
            yield
        finally:
            state_list.remove(worker_thread)


pool = ThreadPool(10)


def callback(status, result):
    pass


def join_result(array_result):
    lines = []
    for i in array_result:
        if i != "\n":
            lines.append(i)
        else:
            yield "".join(lines)
            lines = []


def action(ip):

    cmd = "ping -c 4 "

    (array_state, array_result) = commands.getstatusoutput(cmd + ip)        # run ping cmd + host_ip
    if array_state == 0 and array_result is not None:                       # the cmd is run OK
        for line in join_result(array_result + "\n"):
            if "packets transmitted" in line.strip():
                received = line.strip().split(",")[1].strip().split()[0]
                received = int(received)
                if received == 0:           # 说明不通  4个包都不可达
                    q = "%s: error" % ip
                    task_queue.put(q)
                else:
                    q = "%s: OK!" % ip
                    r = {"state": "0", "re":q}
                    task_queue.put(r)
    else:                                                                   # 命令运行失败
        for line in join_result(array_result + "\n"):
            if "packets transmitted" in line.strip():
                received = line.strip().split(",")[1].strip().split()[0]
                received = int(received)
                if received == 0:           # 说明不通  4个包都不可达
                    q = "%s: error" % ip
                    r = {"state": "1", "re":q}
                    task_queue.put(r)
                else:
                    q = "%s: OK!" % ip
                    task_queue.put(q)


def run_ping_by_ip(ip_list):
    print "ips_______list___in", ip_list
    re_list = []
    for ip in ip_list:
        ret = pool.run(action, (ip,), callback)

    # time.sleep(2)
    pool.close()
    # pool.terminate()
    print "66666666666666666666666666666"
    while True:

        v = task_queue.get()        # 从队列中获取一个值 阻塞的方式
        print "vvvvvvvvvvvvvvvvvvvvvvvv", v
        if v:
            re_list.append(v)
        if task_queue.qsize() == 0:
            break
    return re_list
