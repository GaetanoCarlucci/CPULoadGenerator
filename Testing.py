#!/usr/bin/python

#Authors: Gaetano Carlucci
#         Giuseppe Cofano


import multiprocessing
from twisted.python import usage

from Monitor import MonitorThread
from Controller import ControllerThread
from Actuator import Actuator
 
if __name__ == "__main__":
   
    monitor = MonitorThread(options['cpu'])       
    monitor.start()

    control = ControllerThread()
    control.start()
    control.setCpuTarget(options['cpuLoad'])

    ######################################################
    #             IDENTIFICATION TEST                    #
    ######################################################
    # testing activities
    # this test aims at characterizing the CPU
    cpuTest = np.arange(0.1,0.3,0.1)
    print cpuTest
    data = {"x":[], "y":[]}
    for cpu in cpuTest:
        actuator = Actuator(control, monitor, 3, 0, cpu)
        data["x"].append(cpu)
        data["y"].append(actuator.run())
    print data

    monitor.running = 0;
    control.running = 0;
    monitor.join()
    control.join()