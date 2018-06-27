#!/usr/bin/env python

# Authors: Gaetano Carlucci
#         Giuseppe Cofano
# Python3 port: Manuel Olguín

import multiprocessing
from twisted.python import usage

import sys
# sys.path.insert(0, 'utils')

from utils.Monitor import MonitorThread
from utils.Controller import ControllerThread
from utils.ClosedLoopActuator import ClosedLoopActuator

import signal


class Options(usage.Options):
    """
       Defines the default input parameters
    """
    optParameters = [
        ["cpuLoad", "l", 0.2, "Cpu Target Load", float],
        ["duration", "d", 10, "Duration", int],
        ["plot", "p", 0, "Enable Plot", int],
        ["cpu_core", "c", 0, "Select the CPU on which generate the load", int]
    ]


class ShutdownException(Exception):
    pass


def __sig_handler(*args):
    raise ShutdownException()


if __name__ == "__main__":

    options = Options()
    try:
        options.parseOptions()
    except Exception as e:
        print(f'{sys.argv[0]}: {e}')
        print(f'{sys.argv[0]}: Try --help for usage details.')
        sys.exit(1)
    else:
        if options['cpuLoad'] < 0 or options['cpuLoad'] > 1:
            print("CPU target load out of the range [0,1]")
            sys.exit(1)
        if options['duration'] < 0:
            print("Invalid duration")
            sys.exit(1)
        if options['plot'] != 0 and options['plot'] != 1:
            print("plot can be enabled 1 or disabled 0")
            sys.exit(1)
        if options['cpu_core'] >= multiprocessing.cpu_count():
            print(f'You have only {multiprocessing.cpu_count()} '
                  f'cores on your machine')
            sys.exit(1)

    monitor = MonitorThread(options['cpu_core'], 0.1)
    control = ControllerThread(0.1)
    control.set_cpu_target(options['cpuLoad'])
    actuator = ClosedLoopActuator(control, monitor, options['duration'],
                                  options['cpu_core'], options['cpuLoad'],
                                  options['plot'])

    signal.signal(signal.SIGINT, __sig_handler)
    signal.signal(signal.SIGTERM, __sig_handler)

    try:
        monitor.start()
        control.start()

        actuator.run()

    except ShutdownException:
        pass

    finally:
        actuator.close()

        monitor.stop()
        control.stop()

        monitor.join()
        control.join()
