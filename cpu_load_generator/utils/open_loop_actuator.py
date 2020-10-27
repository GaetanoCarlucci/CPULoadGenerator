#Authors: Gaetano Carlucci
#         Giuseppe Cofano

import time

from cpu_load_generator.utils._plot import RealTimePlot


class OpenLoopActuator:
    """
        Generates CPU load by tuning the sleep time
    """
    def __init__(self, monitor, duration, cpu_core, plot):
        self.sleep_time = 0.03
        self.monitor = monitor
        self.duration = duration
        self.plot = plot
        self.period = 0.05 # actuation period  in seconds
        self.cpu_core = cpu_core
        if self.plot:
            self.graph = RealTimePlot(self.duration, cpu_core, 0)

    def close(self):
        if self.plot:
            self.graph.close()

    def _check_sleep_time(self, sleep_time):
        if sleep_time > self.period:
            sleep_time = self.period
        if sleep_time < 0:
            sleep_time = 0
        return sleep_time

    def _generate_load(self, sleep_time):
        interval = time.time() + self.period - sleep_time
        # generates some getCpuLoad for interval seconds
        while time.time() < interval:
            pr = 213123  # generates some load
            pr * pr
            pr += 1

        time.sleep(sleep_time)

    def _send_plot_sample(self):
        if self.plot:
            self.graph.plot_sample(self.monitor.sleep_time_target, 0)

    def run(self):
        duration = time.time() + self.duration
        while time.time() < duration:
            self._generate_load(self._check_sleep_time(self.sleep_time))
            self._send_plot_sample()

    def run_sequence(self, sequence):       
        for sleep_time_target in sequence:
            step_period = time.time() + 4
            self.monitor.sleep_time_target = sleep_time_target
            while time.time() < step_period:
                self._generate_load(self._check_sleep_time(sleep_time_target))
                self._send_plot_sample()
