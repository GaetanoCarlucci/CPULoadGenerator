#!/usr/bin/python

#Authors: Gaetano Carlucci
#         Giuseppe Cofano


import json
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, '../utils')

from Monitor import MonitorThread
from Controller import ControllerThread
from closedLoopActuator import closedLoopActuator
 
if __name__ == "__main__":
   
    ######################################################
    #             ASSISTED IDENTIFICATION TEST           #
    ######################################################
    # testing activities
    # this test aims at characterizing the CPU
    testing = 1
    if testing == 1:
        cpuTest = np.linspace(0.1,0.9,9)
        cpuTest = np.linspace(0.1,0.9,2)
        data = {"x":[], "y":[]}
        for cpuLoad in cpuTest:
            monitor = MonitorThread(0)
            monitor.start()
            control = ControllerThread()
            control.start()
            control.setCpuTarget(cpuLoad)
            actuator = closedLoopActuator(control, monitor, 5, 1, 0, cpuLoad)
            data['x'].append(cpuLoad*100)
            data['y'].append(actuator.run())
            actuator.close()
            monitor.running = 0
            control.running = 0
            monitor.join()
            control.join()
        
        with open('scatter_plot_data_assisted', 'w') as outfile:
            json.dump(data, outfile)
    else:
        with open('scatter_plot_data_assisted', 'r') as outfile:
            data = json.load(outfile)

    plt.figure()
    plt.scatter(data['x'], data['y'])
    plt.xlabel('CPU Target Load (%)')
    plt.ylabel('Sleep Time [ms]')
    plt.grid(True)
    plt.savefig("Assisted_scatter_plot.jpg",dpi=100)
    plt.show()
    