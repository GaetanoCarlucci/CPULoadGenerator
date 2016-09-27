#!/usr/bin/python

#Authors: Gaetano Carlucci
#         Giuseppe Cofano


import time
import json
import matplotlib.pyplot as plt

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../utils')

from Monitor import MonitorThread
from openLoopActuator import openLoopActuator
 
if __name__ == "__main__":
   
    ######################################################
    #             IDENTIFICATION TEST                    #
    ######################################################
    # testing activities
    # this test aims at characterizing the CPU
    testing = 1
    dynamics_plot_online = 0
    if testing == 1:
        sleepTimeSequence = [0.001, 0.005, 0.01, 0.02, 0.03, 0.08, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5]
        sleepTimeSequence = [0.001, 0.03, 0.02, 0.00, 0.04, 0.05, 0.03, 0.01, 0.2, 0.05, 0.01]
        #sleepTimeSequence = [0.005,  0.02]

        stepPeriod = 4
        monitor = MonitorThread(0, 0.1)
        monitor.start()
        actuator = openLoopActuator(monitor, len(sleepTimeSequence) * stepPeriod, 0, dynamics_plot_online)
        actuator.run_sequence(sleepTimeSequence)
        
        monitor.running = 0
        dynamics =  monitor.getDynamics()
        actuator.close()
        monitor.join()
        
        with open('identification_data', 'w') as outfile:
            json.dump(dynamics, outfile)
    else:
        with open('identification_data', 'r') as outfile:
            dynamics = json.load(outfile)

    plt.figure()
    fig, ax1 = plt.subplots()
    ax1.set_ylabel('CPU Load (%)', color='b')
    ax1.plot(dynamics['time'], dynamics['cpu'], 'b-')
    ax1.set_xlabel('Time [ms]')
    ax1.grid(True)
    for tl in ax1.get_yticklabels():
        tl.set_color('b')
    

    ax2 = plt.twinx()
    ax2.set_ylabel('Sleep Time Target(s)', color='r')
    ax2.plot(dynamics['time'], dynamics['sleepTimeTarget'], 'r-')
    ax2.grid(True)
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    plt.savefig('Identification.png', dpi=100)
    plt.close()