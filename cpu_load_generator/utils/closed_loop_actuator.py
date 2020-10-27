# Authors: Gaetano Carlucci
#         Giuseppe Cofano

import time

from cpu_load_generator.utils._plot import RealTimePlot


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
        self.controller.cpu = self.monitor.sleep_time_target
        self.period = 0.05  # actuation period  in seconds
        self.last_plot_time = time.time()
        self.start_time = time.time()
        if self.plot:
            self.graph = RealTimePlot(self.duration, cpu_core, target)

    def run(self):
        while (time.time() - self.start_time) <= self.duration:
            self._run()

    def run_sequence(self, sequence):
        for cpu_target in sequence:
            step_period = time.time() + 4
            self.controller.target_cpu_load = cpu_target
            self.monitor.cpu_target = cpu_target
            while time.time() < step_period:
                self._run()

    def close_plot(self):
        if self.plot:
            self.graph.close()

    def _run(self):
        self.controller.cpu = self.monitor.cpu
        sleep_time = self.controller.sleep_time
        self._generate_load(sleep_time)
        self.monitor.sleep_time = sleep_time
        self._send_plot_sample()

    def _generate_load(self, sleep_time):
        """Generate some CPU load during time period."""
        interval = time.time() + self.period - sleep_time
        # generates some getCpuLoad for interval seconds
        pr = 213123  # generates some load
        while time.time() < interval:
            pr * pr
            pr = pr + 1
        time.sleep(sleep_time)  # controller actuation

    def _send_plot_sample(self):
        if self.plot:
            if time.time() - self.last_plot_time > 0.2:
                self.graph.plot_sample(self.controller.cpu, self.controller.target_cpu_load * 100)
                self.last_plot_time = time.time()
