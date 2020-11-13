from threading import Thread, Event
import time


class ControllerThread(Thread):
    """Controls the CPU status."""

    def __init__(self, target_cpu_load, sampling_interval=0.1, ki=0.2, kp=0.2):
        super(ControllerThread, self).__init__()

        self._target_cpu_load = target_cpu_load  # target CPU load should be provided as input
        self._sampling_interval = sampling_interval

        self.sleep_time = 0.02  # this is controller output: determines the sleep time to achieve the requested CPU load
        self.running = Event()  # thread status

        self._actuation_period = 0.1  # actuation period  in seconds
        self._alpha_filter_coefficient = 0.2  # filter coefficient
        self._current_cpu_load = 0  # current CPU load returned from the Monitor thread
        self._cpu_period = 0.03
        self._ki = ki  # integral constant of th PI regulator
        self._kp = kp  # proportional constant of the PI regulator
        self._integral_error = 0  # integral error

    @property
    def cpu(self):
        return self._current_cpu_load

    @cpu.setter
    def cpu(self, value):
        self._current_cpu_load = self._alpha_filter_coefficient * value + (1 - self._alpha_filter_coefficient) * self._current_cpu_load  # first order filter on the measurement samples

    def run(self):
        self.running.set()
        last_time_stamp = time.time()

        while self.running.is_set():
            time.sleep(self._sampling_interval)
            err = self._target_cpu_load - self.cpu * 0.01  # computes the proportional error

            current_time_stamp = time.time()
            sample_int = current_time_stamp - last_time_stamp

            self._integral_error = self._integral_error + err * sample_int  # computes the integral error
            last_time_stamp = current_time_stamp
            self._cpu_period = self._kp * err + self._ki * self._integral_error

            # anti wind up control
            if self._cpu_period < 0:
                self._cpu_period = 0
                self._integral_error = self._integral_error - err * sample_int
            if self._cpu_period > self._actuation_period:
                self._cpu_period = self._actuation_period
                self._integral_error = self._integral_error - err * sample_int
            self.sleep_time = self._actuation_period - self._cpu_period

