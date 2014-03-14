#!/usr/bin/python

#Authors: Gaetano Carlucci
#         Giuseppe Cofano

import os, psutil,math
import threading
import time

import numpy as np
from collections import deque
import matplotlib.pyplot as plt
from twisted.python import usage

class Options(usage.Options):
    optParameters = [
            ["CPU load", "l", 0.2, None, float],
            ["duration", "d", 20, None, float],
        ]
        
class MonitorThread(threading.Thread):
    def __init__(self):
        self.interval = 0.1;
        self.sample = 0;
        self.cpu = 0;
        self.running = 1;
        self.alpha = 0.1;
        self.cpu_log = list()
        super(MonitorThread, self).__init__()
        
    def get_cpu_load(self):
        return self.cpu
        
    def run(self):
        p = psutil.Process(os.getpid())
        p.set_cpu_affinity([0]) #the process is forced to run only on CPU 0
        while self.running:
            self.sample = p.get_cpu_percent(interval=self.interval)
            self.cpu = self.alpha * self.sample + (1-self.alpha)*self.cpu
            self.cpu_log.append(self.cpu)


class ControllerThread(threading.Thread):
    def __init__(self):
        self.running = 1;
        self.sleepTime = 0.0;
        self.CT = 0.20;    #default value
        self.cpu = 0;
        self.ki = -1;
        self.kp = -0.5;
        self.int_err = 0;
        self.last_ts = time.time();
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
        #through this timer this cycle has the same sampling interval as the cycle in MonitorThread
        while self.running:
           time.sleep(0.1)
           self.err = self.CT - self.cpu*0.01
           ts = time.time()
           
           samp_int = ts - self.last_ts
           self.int_err = self.int_err + self.err*samp_int
           self.last_ts = ts
           self.sleepTime = self.kp*self.err + self.ki*self.int_err
           
           
           if self.sleepTime < 0:
              self.sleepTime = 0;
              self.int_err = self.int_err - self.err*samp_int
              
               
if __name__ == "__main__":

    import sys
    options = Options()
    try:
        options.parseOptions()
    except Exception, e:
        print '%s: %s' % (sys.argv[0], e)
        print '%s: Try --help for usage details.' % (sys.argv[0])
        sys.exit(1)
    else:
        if options['CPU load'] < 0 or options['CPU load'] > 1: 
            raise(ValueError, "CPU load setpoint out of the range [0,1]")
        if options['duration'] < 0: 
            raise(ValueError, "Invalid negative duration")
                
    monitor = MonitorThread()       
    monitor.start()

    SAMPLES=1000;

    control = ControllerThread()
    control.start()
    control.setCpuTarget(options['CPU load'])
    last_ts = time.time()

    a1 = deque([0]*SAMPLES)
    target = deque([0]*SAMPLES)
    tempoReale = deque([0]*SAMPLES)
        
    x = plt.axes(xlim=(0, options['duration']), ylim=(0, 100))

    line1, = plt.plot(a1)
    line2, = plt.plot(target)
    plt.ion()
    plt.ylim([0,100])
    plt.show()
    tempo = 0;

    plt.xlabel('Time(sec)')
    plt.ylabel('CPU load [0] %')
    
    while tempo < options['duration']:

        for i in range(1,2):
           pr = 213123 + 324234 * 23423423

        control.setCpu(monitor.get_cpu_load())
        sleep_time = control.getSleepTime()
        time.sleep(sleep_time)
        
        ts = time.time()
        delta = ts - last_ts
        last_ts = ts
        tempo += delta

        a1.appendleft(monitor.get_cpu_load())
        target.appendleft(control.getCpuTarget()*100)
        tempoReale.appendleft(tempo)
        a1.pop()
        target.pop()
        tempoReale.pop()
        line1.set_ydata(a1)
        line1.set_xdata(tempoReale)
        line2.set_xdata(tempoReale)
        line2.set_ydata(target)
        plt.draw()

    monitor.running = 0;
    control.running = 0;
    monitor.join()
    control.join()
