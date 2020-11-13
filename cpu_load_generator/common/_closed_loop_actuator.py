import time

import os
import psutil


class ClosedLoopActuator:
    """Generates CPU load by tuning the sleep time."""

    def __init__(self, controller, monitor, duration, cpu_core, target):
        self._controller = controller
        self._monitor = monitor
        self._duration = duration
        self._cpu_core = cpu_core
        self._target = target
        self._controller.current_cpu_load = self._monitor.current_cpu_load
        self.period = 0.05  # actuation period  in seconds
        self.start_time = time.time()

        process = psutil.Process(os.getpid())
        process.cpu_affinity([self._cpu_core])

    def run(self):
        process = psutil.Process(os.getpid())
        process.cpu_affinity([self._cpu_core])

        while (time.time() - self.start_time) <= self._duration:
            self._controller.cpu = self._monitor.current_cpu_load
            sleep_time = self._controller.sleep_time
            self._generate_load(sleep_time)

    def _generate_load(self, sleep_time):
        """Generate some CPU load during time period."""
        interval = time.time() + self.period - sleep_time
        counter = 213123  # generates some load
        while time.time() < interval:
            counter * counter
            counter = counter + 1
        time.sleep(sleep_time)  # controller actuation
