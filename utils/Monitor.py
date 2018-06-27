# Authors: Gaetano Carlucci
#         Giuseppe Cofano

import os
import psutil
from threading import Thread, Event
import time


class MonitorThread(Thread):
    """
       Monitors the CPU status
    """

    def __init__(self, cpu_core, interval):
        # synchronization
        self.shutdown_flag = Event()

        self.sampling_interval = interval;  # sample time interval
        self.sample = 0.5;  # cpu load measurement sample
        self.cpu = 0.5;  # cpu load filtered

        self.alpha = 1;  # filter coefficient
        self.sleepTimeTarget = 0.03
        self.sleepTime = 0.03
        self.cpuTarget = 0.5
        self.cpu_core = cpu_core
        self.dynamics = {"time"     : [], "cpu": [], "sleepTimeTarget": [],
                         "cpuTarget": [], "sleepTime": [], }
        super(MonitorThread, self).__init__()

    def stop(self):
        self.shutdown_flag.set()

    def get_cpu_load(self):
        return self.cpu

    def set_sleep_time_target(self, sleep_time_target):
        self.sleepTimeTarget = sleep_time_target

    def set_sleep_time(self, sleep_time):
        self.sleepTime = sleep_time

    def set_cpu_target(self, cpu_target):
        self.cpuTarget = cpu_target

    def get_dynamics(self):
        return self.dynamics

    def run(self):
        start_time = time.time()
        p = psutil.Process(os.getpid())
        try:
            p.set_cpu_affinity([self.cpu_core])
            # the process is forced
            # to run only on the selected CPU
        except AttributeError:
            p.cpu_affinity([self.cpu_core])

        self.shutdown_flag.clear()
        while not self.shutdown_flag.is_set():
            try:
                self.sample = p.get_cpu_percent(self.sampling_interval)
            except AttributeError:
                self.sample = p.cpu_percent(self.sampling_interval)

            self.cpu = self.alpha * self.sample + (
                        1 - self.alpha) * self.cpu  # first order filter on the measurement samples
            # self.cpu_log.append(self.cpu)
            self.dynamics['time'].append(time.time() - start_time)
            self.dynamics['cpu'].append(self.cpu)
            self.dynamics['sleepTimeTarget'].append(self.sleepTimeTarget)
            self.dynamics['sleepTime'].append(self.sleepTime)
            self.dynamics['cpuTarget'].append(self.cpuTarget)
