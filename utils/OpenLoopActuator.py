# Authors: Gaetano Carlucci
#         Giuseppe Cofano

import time

from utils.Plot import RealTimePlot


class OpenLoopActuator:
    """
        Generates CPU load by tuning the sleep time
    """

    def __init__(self, monitor, duration, cpu_core, plot):
        self.sleep_time = 0.03
        self.monitor = monitor
        self.duration = duration
        self.plot = plot
        self.period = 0.05  # actuation period  in seconds
        self.cpu_core = cpu_core
        if self.plot:
            self.graph = RealTimePlot(self.duration, cpu_core, 0)

    def set_sleep_time(self, sleep_time):
        self.sleep_time = sleep_time

    def close(self):
        if self.plot:
            self.graph.close()

    def check_sleep_time(self, sleep_time):
        if sleep_time > self.period:
            sleep_time = self.period
        if sleep_time < 0:
            sleep_time = 0
        return sleep_time

    def generate_load(self, sleep_time):
        interval = time.time() + self.period - sleep_time
        # generates some getCpuLoad for interval seconds
        while time.time() < interval:
            pr = 213123  # generates some load
            _ = pr * pr
            pr = pr + 1

        time.sleep(sleep_time)

    def send_plot_sample(self):
        if self.plot:
            self.graph.plot_sample(self.monitor.get_cpu_load(), 0)

    def run(self):
        duration = time.time() + self.duration
        while time.time() < duration:
            self.generate_load(self.check_sleep_time(self.sleep_time))
            self.send_plot_sample()

    def run_sequence(self, sequence):
        for SleepTimeTarget in sequence:
            step_period = time.time() + 4
            self.monitor.set_sleep_time_target(SleepTimeTarget)
            while time.time() < step_period:
                self.generate_load(self.check_sleep_time(SleepTimeTarget))
                self.send_plot_sample()
