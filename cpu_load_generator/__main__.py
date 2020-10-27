#!/usr/bin/python

#Authors: Gaetano Carlucci
#         Giuseppe Cofano

import argparse

from cpu_load_generator.utils._monitor import MonitorThread
from cpu_load_generator.utils._controller import ControllerThread
from cpu_load_generator.utils.closed_loop_actuator import ClosedLoopActuator


def parse_args(parser):
    parser.add_argument('-l', '--cpu_load', type=float, help='Cpu Target Load')
    parser.add_argument('-d', '--duration', type=int, help='Duration')
    parser.add_argument('-p', '--plot', type=bool, default=False, help='Enable Plot')
    parser.add_argument('-c', '--cpu_core', type=int, help='Select the CPU on which generate the load')
    args = parser.parse_args()

    return args


def main():
    parser = argparse.ArgumentParser()
    args = parse_args(parser)

    monitor = MonitorThread(args.cpu_core, 0.1)
    monitor.start()

    control = ControllerThread(0.1)
    control.start()
    control.target_cpu_load = args.cpu_load

    actuator = ClosedLoopActuator(control, monitor, args.duration, args.cpu_core, args.cpu_load, args.plot)
    actuator.run()
    actuator.close_plot()

    monitor.running = 0
    control.running = 0
    monitor.join()
    control.join()


if __name__ == "__main__":
    main()
