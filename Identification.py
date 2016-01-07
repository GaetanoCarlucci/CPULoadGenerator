#!/usr/bin/python

#Authors: Gaetano Carlucci
#         Giuseppe Cofano


import json
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, 'utils')

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
        sleepTimeTest = [0.02, 0.05, 0.1, 0.12, 0.15, 0.18, 0.2, 0.22, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]
        #sleepTimeTest = [0.02, 0.05]
        print sleepTimeTest
        data = {"x":[], "y":[]}
        for sleepTime in sleepTimeTest:
            monitor = MonitorThread(0)
            monitor.start()
            actuator = openLoopActuator(monitor, 5, 1, 0, 0)
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
    