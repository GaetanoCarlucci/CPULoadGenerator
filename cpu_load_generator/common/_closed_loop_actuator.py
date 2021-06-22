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

    @property
    def duration_s(self):
        """"Get CPU load duration.

        returns: duration of CPU load.

        """
        return self._duration_s

    @duration_s.setter
    def duration_s(self, duration_s):
        """Set duration of CPU load.

        param duration_s: duration of CPU load in seconds
        type duration_s: int, float

        """
        self._duration_s = duration_s

    @property
    def cpu_target(self):
        """Get CPU load target.

        returns: CPU load target.

        """
        return self._cpu_target

    @cpu_target.setter
    def cpu_target(self, target_cpu_load):
        """Set target CPU load.

        param target_cpu_load: target CPU load as fractions of 1
        type target_cpu_load: float

        """
        self._cpu_target = target_cpu_load

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
