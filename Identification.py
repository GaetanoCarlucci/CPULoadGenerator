#!/usr/bin/python

#Authors: Gaetano Carlucci
#         Giuseppe Cofano


from twisted.python import usage
import json
import numpy as np
import matplotlib.pyplot as plt

from Monitor import MonitorThread
from Controller import ControllerThread
from bareActuator import bareActuator
 
if __name__ == "__main__":
   
    ######################################################
    #             IDENTIFICATION TEST                    #
    ######################################################
    # testing activities
    # this test aims at characterizing the CPU
    testing = 1
    if testing == 1:
        sleepTimeTest = [0.1, 0.12, 0.15, 0.18, 0.2, 0.22, 0.25, 0.3, 0.35, 0.4, 0.45]
        print sleepTimeTest
        data = {"x":[], "y":[]}
        for sleepTime in sleepTimeTest:
            monitor = MonitorThread(0)
            monitor.start()
            actuator = bareActuator(monitor, 5, 1, 0, 0)
            actuator.setSleepTime(sleepTime)
            data['x'].append(sleepTime)
            data['y'].append(actuator.run())
            actuator.close()
            monitor.running = 0
            monitor.join()
        
        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile)
    else:
        with open('data.txt', 'r') as outfile:
            data = json.load(outfile)

    plt.figure()
    plt.scatter(data['x'], data['y'])
    plt.ylabel('CPU Load (%)')
    plt.xlabel('Sleep Time [ms]')
    plt.grid(True)
    plt.savefig("Scatter_plot_without_PID.jpg",dpi=100)
    plt.show()
    