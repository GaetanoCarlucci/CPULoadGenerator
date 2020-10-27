# Authors: Gaetano Carlucci
#         Giuseppe Cofano

import threading
import time


class ControllerThread(threading.Thread):
    """Controls the CPU status."""

    def __init__(self, interval, ki=0.2, kp=0.2):
        self.running = 1  # thread status
        self.sampling_interval = interval
        self.period = 0.1  # actuation period  in seconds
        self.sleep_time = 0.02  # this is controller output: determines the sleep time to achieve the requested CPU load
        self.alpha = 0.2  # filter coefficient
        self.target_cpu_load = 0.20  # target CPU load should be provided as input
        self._cpu = 0  # current CPU load returned from the Monitor thread
        self.cpu_period = 0.03
        self.ki = ki  # integral constant of th PI regulator
        self.kp = kp  # proportional constant of the PI regulator
        self.int_err = 0  # integral error
        self.last_ts = time.time()  # last sampled time
        super(ControllerThread, self).__init__()

    @property
    def cpu(self):
        return self._cpu

    @cpu.setter
    def cpu(self, value):
        self._cpu = self.alpha * value + (1 - self.alpha) * self._cpu  # first order filter on the measurement samples

    def run(self):
        while self.running:
            # ControllerThread has to have the same sampling interval as MonitorThread
            time.sleep(self.sampling_interval)
            err = self.target_cpu_load - self.cpu * 0.01  # computes the proportional error
            ts = time.time()

            sample_int = ts - self.last_ts
            self.int_err = self.int_err + err * sample_int  # computes the integral error
            self.last_ts = ts
            self.cpu_period = self.kp * err + self.ki * self.int_err

            # anti wind up control
            if self.cpu_period < 0:
                self.cpu_period = 0
                self.int_err = self.int_err - err * sample_int
            if self.cpu_period > self.period:
                self.cpu_period = self.period
                self.int_err = self.int_err - err * sample_int
            self.sleep_time = self._cpu_model(self.cpu_period)

    def _cpu_model(self, cpu_period):
        sleep_time = self.period - cpu_period
        return sleep_time
