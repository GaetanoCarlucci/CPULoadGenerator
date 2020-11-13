import time

import os
import psutil


class ClosedLoopActuator:
    """Generates CPU load by tuning the sleep time."""

    def __init__(self, controller, monitor, duration_s, cpu_core_num, cpu_target):
        self._controller = controller
        self._monitor = monitor
        self._duration_s = duration_s
        self._cpu_core_num = cpu_core_num
        self._cpu_target = cpu_target

        self._actuation_period = 0.05

    def run(self):
        process = psutil.Process(os.getpid())
        process.cpu_affinity([self._cpu_core_num])
        start_time = time.time()

        while (time.time() - start_time) <= self._duration_s:
            self._controller.cpu = self._monitor.current_cpu_load
            sleep_time = self._controller.sleep_time_s
            self._generate_load(sleep_time)

    def _generate_load(self, sleep_time):
        """Generate some CPU load during time period."""
        interval = time.time() + self._actuation_period - sleep_time
        counter = 213123  # generates some load
        while time.time() < interval:
            counter * counter
            counter = counter + 1
        time.sleep(sleep_time)  # controller actuation
