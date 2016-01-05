#Authors: Gaetano Carlucci
#         Giuseppe Cofano

import os, psutil
import threading
       
class MonitorThread(threading.Thread):
    """
       Monitors the CPU status
    """
    def __init__(self, cpu):
        self.interval = 0.1; # sample time interval
        self.sample = 0; # cpu load measurement sample
        self.cpu = 0; # cpu load filtered
        self.running = 1; # thread status
        self.alpha = 0.1; # filter coefficient
        self.cpu = cpu
        # self.cpu_log = list() 
        super(MonitorThread, self).__init__()
        
    def getCpuLoad(self):
        return self.cpu
        
    def run(self):
        p = psutil.Process(os.getpid())
        p.set_cpu_affinity([self.cpu]) #the process is forced to run only on the selected CPU
        while self.running:
            self.sample = p.get_cpu_percent(interval=self.interval)
            self.cpu = self.alpha * self.sample + (1 - self.alpha)*self.cpu # first order filter on the measurement samples
            #self.cpu_log.append(self.cpu)