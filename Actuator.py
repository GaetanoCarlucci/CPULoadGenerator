#Authors: Gaetano Carlucci
#         Giuseppe Cofano

import time
import matplotlib.pyplot as plt

from Plot import realTimePlot

class Actuator():
    """
        Generates CPU load by tuning the sleep time
    """
    def __init__(self, controller, monitor, duration, plot, cpu, target):
        self.running = 1;  # thread status
        self.controller = controller
        self.monitor = monitor
        self.duration = duration
        self.plot = plot
        self.start_time = time.time()
        if self.plot:
            self.graph = realTimePlot(self.duration, cpu, target)

    def close(self):
        if self.plot:
            self.graph.close()
           
    def run(self):
        while (time.time() - self.start_time) <= self.duration:
       
            for i in range(1,2):
                pr = 213123 + 324234 * 23423423 # generates some load
            
            self.controller.setCpu(self.monitor.getCpuLoad())
            sleep_time = self.controller.getSleepTime()
            time.sleep(sleep_time) # controller actuation

            if self.plot:
                self.graph.plotSample(self.monitor.getCpuLoad(), self.controller.getCpuTarget()*100)
        return sleep_time