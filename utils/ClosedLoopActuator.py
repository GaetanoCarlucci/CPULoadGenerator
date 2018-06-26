# Authors: Gaetano Carlucci
#         Giuseppe Cofano

import time

from utils.Plot import RealTimePlot


class ClosedLoopActuator:
    """
        Generates CPU load by tuning the sleep time
    """

    def __init__(self, controller, monitor, duration, cpu_core, target, plot):
        self.controller = controller
        self.monitor = monitor
        self.duration = duration
        self.plot = plot
        self.target = target
        self.controller.set_cpu(self.monitor.get_cpu_load())
        self.period = 0.05  # actuation period  in seconds
        self.last_plot_time = time.time()
        self.start_time = time.time()
        if self.plot:
            self.graph = RealTimePlot(self.duration, cpu_core, target)

    # Redefined further down!
    # def generate_load(self, sleep_time):
    #     interval = time.time() + self.cycle - sleep_time
    #     # generates some getCpuLoad for interval seconds
    #     while (time.time() < interval):
    #         pr = 213123  # generates some load
    #         pr * pr
    #         pr = pr + 1
    #     time.sleep(sleep_time) # controller actuation

    def send_plot_sample(self):
        if self.plot:
            if (time.time() - self.last_plot_time) > 0.2:
                self.graph.plot_sample(self.controller.get_cpu(),
                                       self.controller.get_cpu_target() * 100)
                self.last_plot_time = time.time()

    def close(self):
        if self.plot:
            self.graph.close()

    def generate_load(self, sleep_time):
        interval = time.time() + self.period - sleep_time
        # generates some getCpuLoad for interval seconds
        while time.time() < interval:
            pr = 213123  # generates some load
            _ = pr * pr
            pr = pr + 1

        time.sleep(sleep_time)

    def run(self):
        sleep_time = 0
        while (time.time() - self.start_time) <= self.duration:
            self.controller.set_cpu(self.monitor.get_cpu_load())
            sleep_time = self.controller.get_sleep_time()
            self.generate_load(sleep_time)
            self.send_plot_sample()
        return sleep_time

    def run_sequence(self, sequence):
        for cpuTarget in sequence:
            step_period = time.time() + 4
            self.controller.set_cpu_target(cpuTarget)
            self.monitor.set_cpu_target(cpuTarget)
            while time.time() < step_period:
                self.controller.set_cpu(self.monitor.get_cpu_load())
                sleep_time = self.controller.get_sleep_time()
                self.generate_load(sleep_time)
                self.monitor.set_sleep_time(sleep_time)
                self.send_plot_sample()
