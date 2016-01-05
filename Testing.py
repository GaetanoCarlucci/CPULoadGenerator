#!/usr/bin/python

#Authors: Gaetano Carlucci
#         Giuseppe Cofano


from twisted.python import usage
import json
import numpy as np
import matplotlib.pyplot as plt

from Monitor import MonitorThread
from Controller import ControllerThread
from Actuator import Actuator
 
if __name__ == "__main__":
   
    ######################################################
    #             IDENTIFICATION TEST                    #
    ######################################################
    # testing activities
    # this test aims at characterizing the CPU
    testing = 1
    if testing == 1:
        cpuTest = np.arange(0.1,1,0.1)
        data = {"x":[], "y":[]}
        for cpuLoad in cpuTest:
            monitor = MonitorThread(0)
            monitor.start()
            control = ControllerThread()
            control.start()
            control.setCpuTarget(cpuLoad)
            actuator = Actuator(control, monitor, 5, 1, 0, cpuLoad)
            data['x'].append(cpuLoad*100)
            data['y'].append(actuator.run())
            actuator.close()
            monitor.running = 0
            control.running = 0
            monitor.join()
            control.join()
        
        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile)
    else:
        with open('data.txt', 'r') as outfile:
            data = json.load(outfile)

    plt.figure()
    plt.scatter(data['x'], data['y'])
    plt.xlabel('CPU Target Load (%)')
    plt.ylabel('Sleep Time [ms]')
    plt.grid(True)
    plt.savefig("Scatter_plot.jpg",dpi=100)
    plt.show()
    