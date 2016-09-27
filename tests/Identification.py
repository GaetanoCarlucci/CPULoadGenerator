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

period = 0.05 

def cpu_model(cpu_target):
    cpu_time = cpu_target * period
    sleepTime = period - cpu_time
    return sleepTime
 
if __name__ == "__main__":
    cpuSequence = [0.1, 0.8, 0.30, 0.70, 0.40, 0.10, 0.20, 0.60, 0.20, 0.70]
    ######################################################
    #             IDENTIFICATION TEST                    #
    ######################################################
    # testing activities
    # this test aims at characterizing the CPU
    testing = 1
    dynamics_plot_online = 0
    if testing == 1:
    
        sleepTimeTest = [ cpu_model(x) for x in cpuSequence]

        data = {"x":[], "y":[]}
        for sleepTime in sleepTimeTest:
            monitor = MonitorThread(0, 0.1)
            monitor.setSleepTimeTarget(sleepTime)
            monitor.start()

            actuator = openLoopActuator(monitor, 10, 0, dynamics_plot_online)
            actuator.setSleepTime(sleepTime)
            actuator.run()
            
            monitor.running = 0
            dynamics =  monitor.getDynamics()
            actuator.close()
            monitor.join()

            data['x'].append(sleepTime)
            data['y'].append(sum(dynamics['cpu']) / float(len(dynamics['cpu'])))

            monitor.running = 0
            monitor.join()

            if not dynamics_plot_online:
                plt.figure()
                plt.plot(dynamics['time'], dynamics['cpu'])
                plt.ylabel('CPU Load (%)')
                plt.xlabel('Time [ms]')
                plt.title('Dynamics_sleep_time_%fs.png' % (sleepTime))
                plt.grid(True)
                plt.savefig('Dynamics_sleep_time_%fs.png' % (sleepTime),dpi=100)
                plt.close()
        
        with open('scatter_plot_data', 'w') as outfile:
            json.dump(data, outfile)
    else:
        with open('scatter_plot_data', 'r') as outfile:
            data = json.load(outfile)

    plt.figure()

    plt.scatter(data['x'], data['y'])
    plt.ylabel('CPU Load (%)')
    plt.xlabel('Sleep Time [ms]')
    plt.grid(True)
    plt.savefig("Scatter_plot2.png",dpi=100)
    plt.show()

    cpu_time = [ (period*x) for x in cpuSequence]
    plt.scatter(cpu_time, data['y'])
    plt.ylabel('CPU Load (%)')
    plt.xlabel('CPU fraction Time [ms]')
    plt.grid(True)
    plt.savefig("Scatter_plot.png",dpi=100)
    plt.show()