#Authors: Gaetano Carlucci
#         Giuseppe Cofano

import time

from Plot import realTimePlot

class closedLoopActuator():
    """
        Generates CPU load by tuning the sleep time
    """
    def __init__(self, controller, monitor, duration, plot, cpu, target):
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

            interval = time.time() + 0.01
       
            # generates some getCpuLoad for interval seconds
            while (time.time() < interval):
                pr = 213123  # generates some load
                pr * pr
                pr = pr + 1

            self.controller.setCpu(self.monitor.getCpuLoad())
            sleep_time = self.controller.getSleepTime()
            time.sleep(sleep_time) # controller actuation

            if self.plot:
                self.graph.plotSample(self.monitor.getCpuLoad(), self.controller.getCpuTarget()*100)
        return sleep_time