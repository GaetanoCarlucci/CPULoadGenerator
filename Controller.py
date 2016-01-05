#Authors: Gaetano Carlucci
#         Giuseppe Cofano

import threading
import time

class ControllerThread(threading.Thread):
    """
        Controls the CPU status
    """
    def __init__(self):
        self.running = 1;  # thread status
        self.sleepTime = 0.0; # this is controller output: determines the sleep time to achieve the requested CPU load
        self.CT = 0.20;    # target CPU load should be provided as input 
        self.cpu = 0;   # current CPU load returned from the Monitor thread
        self.ki = -1;   # integral constant of th PI regulator (the plant is an inverter)
        self.kp = -0.5; # proportional constant of th PI regulator (the plant is an inverter)
        self.int_err = 0;  # integral error
        self.last_ts = time.time();  # last sampled time
        super(ControllerThread, self).__init__()
        
    def getSleepTime(self):
        return self.sleepTime

    def getCpuTarget(self):
        return self.CT

    def setCpu(self, cpu): 
       self.cpu = cpu

    def setCpuTarget(self, CT): 
       self.CT = CT
     
    def run(self):
        while self.running:
           # ControllerThread has to have the same sampling interval as MonitorThread
           time.sleep(0.1)
           self.err = self.CT - self.cpu*0.01  # computes the proportional error
           ts = time.time()
           
           samp_int = ts - self.last_ts  # sample interval 
           self.int_err = self.int_err + self.err*samp_int  # computes the integral error
           self.last_ts = ts
           self.sleepTime = self.kp*self.err  + self.ki*self.int_err
           
           #anti wind up control
           if self.sleepTime < 0:
              self.sleepTime = 0;
              self.int_err = self.int_err - self.err*samp_int