# Authors: Gaetano Carlucci
#         Giuseppe Cofano

import time

from Plot import realTimePlot


class closedLoopActuator():
    """
        Generates CPU load by tuning the sleep time
    """

    def __init__(self, controller, monitor, duration, cpu_core, target, plot):
        self.controller = controller
        self.monitor = monitor
        self.duration = duration
        self.plot = plot
        self.target = target
        self.controller.setCpu(self.monitor.getCpuLoad())
        self.period = 0.05  # actuation period  in seconds
        self.last_plot_time = time.time()
        self.start_time = time.time()
        if self.plot:
            self.graph = realTimePlot(self.duration, cpu_core, target)

    def generate_load(self, sleep_time):
        interval = time.time() + self.cycle - sleep_time
        # generates some getCpuLoad for interval seconds
        while (time.time() < interval):
            pr = 213123  # generates some load
            pr * pr
            pr = pr + 1
        time.sleep(sleep_time)  # controller actuation

    def sendPlotSample(self):
        if self.plot:
            if (time.time() - self.last_plot_time) > 0.2:
                self.graph.plotSample(self.controller.getCpu(), self.controller.getCpuTarget() * 100)
                self.last_plot_time = time.time()

    def close(self):
        if self.plot:
            self.graph.close()

    def generate_load(self, sleep_time):
        interval = time.time() + self.period - sleep_time
        # generates some getCpuLoad for interval seconds
        while (time.time() < interval):
            pr = 213123  # generates some load
            pr * pr
            pr = pr + 1

        time.sleep(sleep_time)

    def run(self):
        while (time.time() - self.start_time) <= self.duration:
            self.controller.setCpu(self.monitor.getCpuLoad())
            sleep_time = self.controller.getSleepTime()
            self.generate_load(sleep_time)
            self.sendPlotSample()
        return sleep_time

    def run_sequence(self, sequence):
        for cpuTarget in sequence:
            stepPeriod = time.time() + 4
            self.controller.setCpuTarget(cpuTarget)
            self.monitor.setCPUTarget(cpuTarget)
            while (time.time() < stepPeriod):
                self.controller.setCpu(self.monitor.getCpuLoad())
                sleep_time = self.controller.getSleepTime()
                self.generate_load(sleep_time)
                self.monitor.setSleepTime(sleep_time)
                self.sendPlotSample()