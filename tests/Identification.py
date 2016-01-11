#!/usr/bin/python

#Authors: Gaetano Carlucci
#         Giuseppe Cofano


import json
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, '../utils')

from Monitor import MonitorThread
from openLoopActuator import openLoopActuator
 
if __name__ == "__main__":
   
    ######################################################
    #             IDENTIFICATION TEST                    #
    ######################################################
    # testing activities
    # this test aims at characterizing the CPU
    testing = 1
    if testing == 1:
        sleepTimeTest = [0.001, 0.005, 0.01, 0.02, 0.03, 0.08, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5]
        #sleepTimeTest = [0.02, 0.05]
        data = {"x":[], "y":[]}
        for sleepTime in sleepTimeTest:
            monitor = MonitorThread(0, 0.1)
            monitor.start()
            actuator = openLoopActuator(monitor, 10, 0, 0, 0)
            actuator.setSleepTime(sleepTime)
            data['x'].append(sleepTime)
            data['y'].append(actuator.run())
            actuator.close()
            monitor.running = 0
            monitor.join()
        
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
    plt.savefig("Scatter_plot.jpg",dpi=100)
    plt.show()