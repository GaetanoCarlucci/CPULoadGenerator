#Authors: Gaetano Carlucci
#         Giuseppe Cofano

import time

from Plot import realTimePlot

class openLoopActuator():
    """
        Generates CPU load by tuning the sleep time
    """
    def __init__(self, monitor, duration, plot, cpu, target):
        self.sleep_time = 0.1;
        self.plot = plot
        self.monitor = monitor
        self.duration = duration
        self.cpuInput = target
        self.start_time = time.time()

        if self.plot:
            self.graph = realTimePlot(self.duration, cpu, target)

    def setSleepTime(self, sleep_time):
        self.sleep_time = sleep_time

    def setCpuInput(self, cpuT):
        self.cpuInput = cpuInput

    def close(self):
        if self.plot:
            self.graph.close()
           
    def run(self):
        while (time.time() - self.start_time) <= self.duration:

            interval = time.time() + 0.01
       
            # generates some getCpuLoad for interval seconds
            while (time.time() < interval):
                pr = 213123  # generates some load
                pr * pr
                pr = pr + 1
            
            
            time.sleep(self.sleep_time) # controller actuation

            if self.plot:
                self.graph.plotSample(self.monitor.getCpuLoad(), self.cpuInput)
        return self.monitor.getCpuLoad()