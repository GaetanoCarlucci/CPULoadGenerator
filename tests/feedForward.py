#!/usr/bin/python

#Authors: Gaetano Carlucci
#         Giuseppe Cofano


import json
import matplotlib.pyplot as plt

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../utils')

from Monitor import MonitorThread
from openLoopActuator import openLoopActuator

period = 0.05 # actuation period  in seconds

def cpu_model(cpu_target):
    cpu_time = cpu_target * period
    sleepTime = period - cpu_time
    return sleepTime

def inverse_cpu_model(sleepTime):
    cpu_model = period - sleepTime
    cpu_load =  cpu_model/period
    return cpu_load

if __name__ == "__main__":
   
    ######################################################
    #             FEEDFORWARD TEST                    #
    ######################################################
    # testing activities
    # this test aims at characterizing the CPU
    testing = 1
    dynamics_plot_online = 0
    if testing == 1:
        sleepTimeSequence = [0.001, 0.005, 0.01, 0.02, 0.03, 0.08, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5]
        cpuSequence = [0.1, 0.8, 0.30, 0.70, 0.40, 0.10, 0.20, 0.60, 0.20, 0.70]
        #cpuSequence = [ 0.80]
        #sleepTimeSequence = [0.001,  0.02]
        sleepTimeSequence = [ cpu_model(x) for x in cpuSequence]
        stepPeriod = 4
        monitor = MonitorThread(0, 0.1)
        actuator = openLoopActuator(monitor, len(sleepTimeSequence) * stepPeriod, 0, dynamics_plot_online)
        monitor.start()
        actuator.run_sequence(sleepTimeSequence)
        
        monitor.running = 0
        dynamics =  monitor.getDynamics()
        actuator.close()
        monitor.join()
        
        with open('feed_forward_data', 'w') as outfile:
            json.dump(dynamics, outfile)
    else:
        with open('feed_forward_data', 'r') as outfile:
            dynamics = json.load(outfile)

    plt.figure()
    fig, ax1 = plt.subplots()
    ax1.set_ylabel('CPU Load (%)', color='b')
    ax1.plot(dynamics['time'], dynamics['cpu'], 'b-')
    ax1.set_xlabel('Time [ms]')
    ax1.grid(True)
    ax1.set_ylim([0, 100])
    for tl in ax1.get_yticklabels():
        tl.set_color('b')
    
    ax2 = plt.twinx()
    ax2.set_ylabel('Input Load', color='r')
    cpuInput = [ 100*inverse_cpu_model(x) for x in dynamics['sleepTimeTarget']]
    ax2.plot(dynamics['time'], cpuInput, 'r-')
    ax2.grid(True)
    ax2.set_ylim([0, 100])
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    plt.savefig('FeedForward.png', dpi=100)
    plt.close()