#!/usr/bin/python

#Authors: Gaetano Carlucci
#         Giuseppe Cofano

import time
import matplotlib.pyplot as plt

from Plot import realTimePlot

class Actuator():
    """
        Generates CPU load by tuning the sleep time
    """
    def __init__(self, controller, monitor, duration, plot, cpuT):
        self.running = 1;  # thread status
        self.controller = controller
        self.monitor = monitor
        self.duration = duration
        self.plot = plot
        self.cpuTarget = cpuT
        self.start_time = time.time()
        if self.plot:
            self.graph = realTimePlot(self.duration, self.cpuTarget)
           
    def run(self):
        # ControllerThread has to have the same sampling interval as MonitorThread
        while (time.time() - self.start_time) <= self.duration:
       
            for i in range(1,2):
                pr = 213123 + 324234 * 23423423 # generates some load
            
            if self.plot:
                self.graph.plotSample(self.monitor.getCpuLoad(), self.controller.getCpuTarget()*100)
            
            self.controller.setCpu(self.monitor.getCpuLoad())
            sleep_time = self.controller.getSleepTime()
            time.sleep(sleep_time) # controller actuation
        return sleep_time