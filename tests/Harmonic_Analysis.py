#!/usr/bin/python

#Authors: Gaetano Carlucci
#         Giuseppe Cofano


import json
import os.path
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, '../utils')

from Monitor import MonitorThread
from Controller import ControllerThread
from Actuator import Actuator
 
if __name__ == "__main__":
   
    ######################################################
    #             HARMONIC ANALYSIS TEST                 #
    ######################################################
    # testing activities
    # this test aims at characterizing the CPU in frequency
    if not  os.path.isfile("data.txt"):
        print "You need to run Testing first!"
        exit()
    
    with open('data.txt', 'r') as outfile:
            data = json.load(outfile)
    
    xInterLoad = np.linspace(10, 90, 50)
    yInterSpleep = np.interp(xInterLoad, data['x'], data['y'])
    
    # for cpuLoad in cpuTest:
    #     monitor = MonitorThread(0)
    #     monitor.start()
    #     control = ControllerThread()
    #     control.start()
    #     control.setCpuTarget(cpuLoad)
    #     actuator = Actuator(control, monitor, 5, 1, 0, cpuLoad)
    #     data['x'].append(cpuLoad*100)
    #     data['y'].append(actuator.run())
    #     actuator.close()
    #     monitor.running = 0
    #     control.running = 0
    #     monitor.join()
    #     control.join()

    plt.figure()
    plt.scatter(data['x'], data['y'])
    plt.scatter(xInterLoad, yInterSpleep)
    plt.xlabel('CPU Target Load (%)')
    plt.ylabel('Sleep Time [ms]')
    plt.grid(True)
    plt.savefig("Scatter_plot.jpg",dpi=100)
    plt.show()


    