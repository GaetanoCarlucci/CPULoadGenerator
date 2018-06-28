#!/usr/bin/env python

#Authors: Gaetano Carlucci
#         Giuseppe Cofano


import json
import matplotlib.pyplot as plt

import sys
import os

import psutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')

from utils.Monitor import MonitorThread
from utils.Controller import ControllerThread
from utils.ClosedLoopActuator import ClosedLoopActuator

if __name__ == "__main__":

    ######################################################
    #             PID TEST                               # 
    ######################################################
    # testing activities
    # this test aims at characterizing the CPU
    testing = 1
    dynamics_plot_online = 0
    p = psutil.Process(os.getpid())
    available_cores = p.cpu_affinity()
    core = available_cores[0]

    if testing == 1:
        cpuSequence = [0.8, 0.1, 0.30, 0.70, 0.40, 0.10, 0.20, 0.60, 0.20, 0.70]
        #cpuSequence = [0.8, 0.1]
        stepPeriod = 4

        control = ControllerThread(0.1)
        monitor = MonitorThread(core, 0.1)
        actuator = ClosedLoopActuator(control, monitor, len(cpuSequence) *
                                      stepPeriod, 1)

        monitor.start()
        control.start()
        actuator.run_sequence(cpuSequence)

        actuator.close()
        monitor.stop()
        control.stop()
        dynamics = monitor.get_dynamics()

        monitor.join()
        control.join()

        stepPeriod = 4

        with open('pid_data', 'w') as outfile:
            json.dump(dynamics, outfile)
    else:
        with open('pid_data', 'r') as outfile:
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
    cpuInput = [ 100*(x) for x in dynamics['cpuTarget']]
    ax2.plot(dynamics['time'], cpuInput, 'r-')
    ax2.grid(True)
    ax2.set_ylim([0, 100])
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    plt.savefig('PID.png', dpi=100)
    plt.close()

    plt.figure()
    plt.plot(dynamics['time'], dynamics['sleepTime'])
    plt.ylabel('PID Actuation - sleepTime (sec)')
    plt.xlabel('Time [ms]')
    plt.title('PID Actuation')
    plt.grid(True)
    plt.savefig('PID Actuation.png',dpi=100)
    plt.close()
