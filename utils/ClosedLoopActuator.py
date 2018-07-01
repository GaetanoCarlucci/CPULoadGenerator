# Authors: Gaetano Carlucci
#         Giuseppe Cofano
import os
import time

import psutil

from utils.Plot import RealTimePlot


class ClosedLoopActuator:
    """
        Generates CPU load by tuning the sleep time
    """

    def __init__(self, controller, monitor, duration, target):
        self.controller = controller
        self.monitor = monitor
        self.duration = duration
        self.target = target
        self.controller.set_cpu(self.monitor.get_cpu_load())
        self.period = 0.05  # actuation period  in seconds
        self.last_plot_time = time.time()
        self.start_time = time.time()

    def send_plot_sample(self):
        pass  # NOOP

    def close(self):
        pass  # NOOP

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

        while self.duration < 0 \
                or (time.time() - self.start_time) <= self.duration:
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


class PlottingClosedLoopActuator(ClosedLoopActuator):
    """
        Generates CPU load by tuning the sleep time and plots results after run.
        This is implemented through polymorphism to avoid internal
        if-branches which generate additional, non-controlled load.
    """

    def __init__(self, controller, monitor, duration, target):
        super(PlottingClosedLoopActuator,
              self).__init__(controller, monitor, duration, target)

        cpu_core = psutil.Process(os.getpid()).cpu_affinity()[0]
        self.graph = RealTimePlot(self.duration, cpu_core, target)

    def send_plot_sample(self):
        if (time.time() - self.last_plot_time) > 0.2:
            self.graph.plot_sample(self.controller.get_cpu(),
                                   self.controller.get_cpu_target() * 100)
            self.last_plot_time = time.time()

    def close(self):
        self.graph.close()