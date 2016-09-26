#Authors: Gaetano Carlucci
#         Giuseppe Cofano

import os, psutil
import threading
import time

class MonitorThread(threading.Thread):
    """
       Monitors the CPU status
    """
    def __init__(self, cpu_core, interval):
        self.sampling_interval = interval; # sample time interval
        self.sample = 0.5; # cpu load measurement sample
        self.cpu = 0.5; # cpu load filtered
        self.running = 1; # thread status
        self.alpha = 1; # filter coefficient
        self.sleepTimeTarget = 0.03
        self.sleepTime = 0.03
        self.cpuTarget = 0.5
        self.cpu_core = cpu_core
        self.dynamics = {"time":[], "cpu":[], "sleepTimeTarget":[], "cpuTarget":[],  "sleepTime":[],}
        super(MonitorThread, self).__init__()
        
    def getCpuLoad(self):
        return self.cpu

    def setSleepTimeTarget(self, sleepTimeTarget):
        self.sleepTimeTarget = sleepTimeTarget

    def setSleepTime(self, sleepTime):
        self.sleepTime = sleepTime

    def setCPUTarget(self, cpuTarget):
        self.cpuTarget = cpuTarget

    def getDynamics(self):
    	return self.dynamics
        
    def run(self):
    	start_time = time.time()
        p = psutil.Process(os.getpid())
        try:
            p.set_cpu_affinity([self.cpu_core]) #the process is forced to run only on the selected CPU
        except AttributeError:
            p.cpu_affinity([self.cpu_core])
            
        while self.running:
            try:
               self.sample = p.get_cpu_percent(self.sampling_interval)
            except AttributeError:
               self.sample = p.cpu_percent(self.sampling_interval)
               
            self.cpu = self.alpha * self.sample + (1 - self.alpha)*self.cpu # first order filter on the measurement samples
            #self.cpu_log.append(self.cpu)
            self.dynamics['time'].append(time.time() - start_time)
            self.dynamics['cpu'].append(self.cpu)
            self.dynamics['sleepTimeTarget'].append(self.sleepTimeTarget)
            self.dynamics['sleepTime'].append(self.sleepTime)
            self.dynamics['cpuTarget'].append(self.cpuTarget)
