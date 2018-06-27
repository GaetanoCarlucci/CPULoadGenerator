# Authors: Gaetano Carlucci
#         Giuseppe Cofano

from threading import Thread, Event
import time


class ControllerThread(Thread):
    """
        Controls the CPU status
    """

    def __init__(self, interval, ki=None, kp=None):
        # synchronization
        self.shutdown_flag = Event()

        self.running = 1;  # thread status
        self.sampling_interval = interval
        self.period = 0.1  # actuation period  in seconds
        self.sleepTime = 0.02;  # this is controller output: determines the sleep time to achieve the requested CPU load
        self.alpha = 0.2;  # filter coefficient
        self.CT = 0.20;  # target CPU load should be provided as input 
        self.cpu = 0;  # current CPU load returned from the Monitor thread
        self.cpuPeriod = 0.03;
        if ki is None:
            self.ki = 0.2  # integral constant of th PI regulator
        if kp is None:
            self.kp = 0.02  # proportional constant of th PI regulator
        self.int_err = 0;  # integral error
        self.last_ts = time.time();  # last sampled time
        super(ControllerThread, self).__init__()

    def stop(self):
        self.shutdown_flag.set()

    def get_sleep_time(self):
        return self.sleepTime

    def cpu_model(self, cpu_period):
        sleep_time = self.period - cpu_period
        return sleep_time

    def get_cpu_target(self):
        return self.CT

    def set_cpu(self, cpu):
        self.cpu = self.alpha * cpu + (
                    1 - self.alpha) * self.cpu  # first order filter on the measurement samples

    def get_cpu(self):
        return self.cpu

    def set_cpu_target(self, CT):
        self.CT = CT

    def run(self):
        self.shutdown_flag.clear()
        while not self.shutdown_flag.is_set():
            # ControllerThread has to have the same sampling interval as MonitorThread
            time.sleep(self.sampling_interval)
            self.err = self.CT - self.cpu * 0.01  # computes the proportional error
            ts = time.time()

            samp_int = ts - self.last_ts  # sample interval
            self.int_err = self.int_err + self.err * samp_int  # computes the integral error
            self.last_ts = ts
            self.cpuPeriod = self.kp * self.err + self.ki * self.int_err

            # anti wind up control
            if self.cpuPeriod < 0:
                self.cpuPeriod = 0
                self.int_err = self.int_err - self.err * samp_int
            if self.cpuPeriod > self.period:
                self.cpuPeriod = self.period
                self.int_err = self.int_err - self.err * samp_int
            self.sleepTime = self.cpu_model(self.cpuPeriod)
