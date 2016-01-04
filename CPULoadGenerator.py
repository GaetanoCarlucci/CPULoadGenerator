#!/usr/bin/python

#Authors: Gaetano Carlucci
#         Giuseppe Cofano

import os, psutil
import multiprocessing
import threading
import time
import numpy as np
import matplotlib.pyplot as plt
from twisted.python import usage

class Options(usage.Options):
    """
       Defines the default input parameters
    """
    optParameters = [
            ["cpuLoad", "l", 0.2, "Cpu Target Load", float],
            ["duration", "d", 10, "Duration", int],
            ["plot", "p" , 1, "Enable Plot", int],
            ["cpu", "c" , 0, "Select the CPU on which generate the load", int]
        ]
        
class MonitorThread(threading.Thread):
    """
       Monitors the CPU status
    """
    def __init__(self, cpu):
        self.interval = 0.1; # sample time interval
        self.sample = 0; # cpu load measurement sample
        self.cpu = 0; # cpu load filtered
        self.running = 1; # thread status
        self.alpha = 0.1; # filter coefficient
        self.cpu = cpu
        # self.cpu_log = list() 
        super(MonitorThread, self).__init__()
        
    def getCpuLoad(self):
        return self.cpu
        
    def run(self):
        p = psutil.Process(os.getpid())
        p.set_cpu_affinity([self.cpu]) #the process is forced to run only on the selected CPU
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
           self.sleepTime = self.kp*self.err  + self.ki*self.int_err
           
           #anti wind up control
           if self.sleepTime < 0:
              self.sleepTime = 0;
              self.int_err = self.int_err - self.err*samp_int


class Actuator():
    """
        Generates CPU load by tuning the sleep time
    """
    def __init__(self, controller, monitor, duration, plot):
        self.running = 1;  # thread status
        self.controller = controller
        self.monitor = monitor
        self.duration = duration
        self.plot = plot
        self.start_time = time.time()
        if self.plot:
            self.graph = realTimePlot(options['duration'], options['cpu'])
           
    def run(self):
        # ControllerThread has to have the same sampling interval as MonitorThread
        while (time.time() - self.start_time) <= options['duration']:
       
            for i in range(1,2):
                pr = 213123 + 324234 * 23423423 # generates some load
            
            if self.plot:
                self.graph.plotSample(monitor.getCpuLoad(),control.getCpuTarget()*100)
            
            self.controller.setCpu(self.monitor.getCpuLoad())
            print self.monitor.getCpuLoad()
            sleep_time = self.controller.getSleepTime()
            time.sleep(sleep_time) # controller actuation
            print (sleep_time)
            
class realTimePlot():
    """
        Plots the CPU load
    """
    def __init__(self, duration, cpu):
        plt.axis([0, duration, 0, 100])
        plt.ion()
        plt.show()
        plt.xlabel('Time(sec)')
        plt.ylabel('%')
        self.y_load = [0]
        self.y_target = [0]
        self.xdata = [0]
        self.line_target, = plt.plot(self.y_target)
        self.line_load, = plt.plot(self.y_load)
        plt.legend([self.line_target, self.line_load], ["Target CPU", "CPU [%d] Load" % (cpu)], ncol=2)
        plt.grid(True)
        self.ts_start = time.time()

    def plotSample(self, sample, target):
        p_x = time.time() - self.ts_start
        p_load = sample
        p_target = target 
        self.y_load.append(p_load)
        self.y_target.append(p_target)
        self.xdata.append(p_x)
        self.line_target.set_xdata(self.xdata)
        self.line_target.set_ydata(self.y_target)
        self.line_load.set_xdata(self.xdata)
        self.line_load.set_ydata(self.y_load)
        plt.draw()
               
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
        if options['cpuLoad'] < 0 or options['cpuLoad'] > 1: 
            print "CPU target load out of the range [0,1]"
            sys.exit(1)
        if options['duration'] < 0: 
            print "Invalid duration"
            sys.exit(1)
        if options['plot'] != 0 and options['plot'] != 1: 
            print "plot can be enabled 1 or disabled 0"
            sys.exit(1)
        if options['cpu'] >= multiprocessing.cpu_count(): 
            print "You have only %d cores on your machine" % (multiprocessing.cpu_count())
            sys.exit(1)
            

                
    monitor = MonitorThread(options['cpu'])       
    monitor.start()

    control = ControllerThread()
    control.start()
    control.setCpuTarget(options['cpuLoad'])

    actuator = Actuator(control, monitor, options['duration'], options['plot'] )
    actuator.run()

    monitor.running = 0;
    control.running = 0;
    monitor.join()
    control.join()
