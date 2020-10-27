# Authors: Gaetano Carlucci
#         Giuseppe Cofano

import os, psutil
import threading
import time


class MonitorThread(threading.Thread):
    """
       Monitors the CPU status
    """

    def __init__(self, cpu_core, interval):
        self.sampling_interval = interval  # sample time interval
        self.sample = 0.5  # cpu load measurement sample
        self.cpu = 0.5  # cpu load filtered
        self.running = 1  # thread status
        self.alpha = 1  # filter coefficient
        self.sleep_time_target = 0.03
        self.sleep_time = 0.03
        self.cpu_target = 0.5
        self.cpu_core = cpu_core
        self.dynamics = {"time": [], "cpu": [], "sleepTimeTarget": [], "cpuTarget": [], "sleepTime": [], }
        super(MonitorThread, self).__init__()

    def run(self):
        start_time = time.time()
        p = psutil.Process(os.getpid())
        try:
            p.set_cpu_affinity([self.cpu_core])  # the process is forced to run only on the selected CPU
        except AttributeError:
            p.cpu_affinity([self.cpu_core])

        while self.running:
            try:
                self.sample = p.get_cpu_percent(self.sampling_interval)
            except AttributeError:
                self.sample = p.cpu_percent(self.sampling_interval)

            self.cpu = self.alpha * self.sample + (1 - self.alpha) * self.cpu  # first order filter on the measurement samples
            # self.cpu_log.append(self.cpu)
            self.dynamics['time'].append(time.time() - start_time)
            self.dynamics['cpu'].append(self.cpu)
            self.dynamics['sleepTimeTarget'].append(self.sleep_time_target)
            self.dynamics['sleepTime'].append(self.sleep_time)
            self.dynamics['cpuTarget'].append(self.cpu_target)
