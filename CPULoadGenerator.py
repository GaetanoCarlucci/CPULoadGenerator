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
    """
       Defines the default input parameters
    """
    optParameters = [
            ["CPU load", "l", 0.2, None, float],
            ["duration", "d", 10, None, float],
        ]
        
class MonitorThread(threading.Thread):
    """
       Monitors the CPU status
    """
    def __init__(self):
        self.interval = 0.1; # sample time interval
        self.sample = 0; # cpu load measurement sample
        self.cpu = 0; # cpu load filtered
        self.running = 1; # thread status
        self.alpha = 0.1; # filter coefficient
        # self.cpu_log = list() 
        super(MonitorThread, self).__init__()
        
    def getCpuLoad(self):
        return self.cpu
        
    def run(self):
        p = psutil.Process(os.getpid())
        p.set_cpu_affinity([0]) #the process is forced to run only on CPU 0: it can be extended
        while self.running:
            self.sample = p.get_cpu_percent(interval=self.interval)
            self.cpu = self.alpha * self.sample + (1-self.alpha)*self.cpu # first order filter on the measurement samples
            #self.cpu_log.append(self.cpu)


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
        # ControllerThread has to have the same sampling interval as MonitorThread
        while self.running:
           time.sleep(0.1)
           self.err = self.CT - self.cpu*0.01  # computes the proportional error
           ts = time.time()
           
           samp_int = ts - self.last_ts  # sample interval 
           self.int_err = self.int_err + self.err*samp_int  # computes the integral error
           self.last_ts = ts
           self.sleepTime = self.kp*self.err + self.ki*self.int_err # PI regulator output
           
           #anti wind up control
           if self.sleepTime < 0:
              self.sleepTime = 0;
              self.int_err = self.int_err - self.err*samp_int

class realTimeplot():

    def __init__(self):
        plt.axis([0, 100, -10, 10])
        plt.ion()
        plt.show()
        ydata = [0]
        line, = plt.plot(ydata)
        ts_start = time.time()

    def plotSample(time,sample):
        p_x = int(int(time.time())-int(ts_start))
        p_y = sample # keeps getting generated in the loop code
        ydata.append(p_y)
        line.set_xdata(np.arange(len(ydata)))
        line.set_ydata(ydata)
        plt.draw()
        #time.sleep(0.05)
              
               
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
            raise(ValueError, "CPU target load out of the range [0,1]")
        if options['duration'] < 0: 
            raise(ValueError, "Invalid duration")
                
    monitor = MonitorThread()       
    monitor.start()

    control = ControllerThread()
    control.start()
    control.setCpuTarget(options['CPU load'])
    last_ts = time.time()

    #a1 = deque([0]*SAMPLES)
    #target = deque([0]*SAMPLES)
    #tempoReale = deque([0]*SAMPLES)
        
    #x = plt.axes(xlim=(0, options['duration']), ylim=(0, 100))

    #line1, = plt.plot(a1)
    #line2, = plt.plot(target)
    #plt.ion()
    #plt.ylim([0,100])
    #plt.show()
    tempo = 0;

    #plt.xlabel('Time(sec)')
    #plt.ylabel('CPU load [0] %')
    
    while tempo < options['duration']:

        for i in range(1,2):
           pr = 213123 + 324234 * 23423423

        control.setCpu(monitor.getCpuLoad())
        sleep_time = control.getSleepTime()
        time.sleep(sleep_time)
        
        ts = time.time()
        delta = ts - last_ts
        last_ts = ts
        tempo += delta

        graph = realTimeplot()
        graph.plotSample(control.getCpuTarget()*100)

       # a1.appendleft(monitor.getCpuLoad())
      #  target.appendleft(control.getCpuTarget()*100)
      #  tempoReale.appendleft(tempo)
      #  a1.pop()
     #   target.pop()
     #   tempoReale.pop()
     #   line1.set_ydata(a1)
      #  line1.set_xdata(tempoReale)
      #  line2.set_xdata(tempoReale)
     #   line2.set_ydata(target)
    #    plt.draw()

    monitor.running = 0;
    control.running = 0;
    monitor.join()
    control.join()
