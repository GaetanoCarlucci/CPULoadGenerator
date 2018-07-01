#!/usr/bin/env python

# Authors: Gaetano Carlucci
#         Giuseppe Cofano
# Python3 port: Manuel Olguín
import itertools
import multiprocessing
import os
import signal

import click
import psutil

from utils.ClosedLoopActuator import ClosedLoopActuator, \
    PlottingClosedLoopActuator
from utils.Controller import ControllerThread
from utils.Monitor import MonitorThread


class ShutdownException(Exception):
    pass


def __sig_handler(*args):
    raise ShutdownException()


def load_core(target_core, target_load,
              duration_seconds=-1, plot=False,
              sampling_interval=0.1):
    if duration_seconds >= 0:
        print(f'Loading core {target_core} ({target_load * 100.0:0>5.2f}%) for '
              f'{duration_seconds} seconds.')
    else:
        print(f'Loading core {target_core} ({target_load * 100.0:0>5.2f}%) '
              f'until interrupted.')

    if sampling_interval <= 0:
        raise Exception('Negative sampling interval!')

    # lock this process to the target core
    process = psutil.Process(os.getpid())
    process.cpu_affinity([target_core])

    monitor = MonitorThread(target_core, sampling_interval)
    control = ControllerThread(sampling_interval)
    control.set_cpu_target(target_load)

    # polymorphism for plotting
    if plot:
        actuator = PlottingClosedLoopActuator(control, monitor,
                                              duration_seconds, target_core)
    else:
        actuator = ClosedLoopActuator(control, monitor,
                                      duration_seconds, target_core)

    signal.signal(signal.SIGINT, __sig_handler)
    signal.signal(signal.SIGTERM, __sig_handler)

    try:
        monitor.start()
        control.start()

        actuator.run()

    except ShutdownException:
        pass

    finally:
        # shutting down, so ignore any signals
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGTERM, signal.SIG_IGN)

        actuator.close()

        monitor.stop()
        control.stop()

        monitor.join()
        control.join()


def __validate_cpu_load(ctx, param, value):
    for v in value:
        if not 0. <= v <= 1.:
            raise click.BadOptionUsage(f'CPU load {v} out of range [0, 1]')
    return value


def __validate_cpu_core(ctx, param, value):
    p = psutil.Process(os.getpid())
    available_cores = p.cpu_affinity()

    for v in value:
        if v not in available_cores:
            raise click.BadOptionUsage(
                f'Target core ({v}) is not one of the available cores: '
                f'{available_cores}')
    return value


def __validate_sampling_interval(ctx, param, value):
    if value < 0:
        raise click.BadOptionUsage(
            f'Sampling interval cannot be negative ({value}).')
    return value


@click.command()
@click.option('--core', '-c',
              type=int, callback=__validate_cpu_core,
              required=True, multiple=True,
              help='CPU core to artificially load. '
                   'Can be specified multiple times to load multiple cores, '
                   'default is all cores.',
              default=psutil.Process(os.getpid()).cpu_affinity(),
              show_default=True)
@click.option('--cpu_load', '-l',
              type=float, multiple=True,
              help='Target CPU load. If only one value is provided, '
                   'it is applied to all affected cores, otherwise specifies '
                   'load per affected core.',
              default=[0.2], show_default=True, callback=__validate_cpu_load)
@click.option('--duration', '-d',
              type=float, default=-1, show_default=True,
              help='Duration in seconds. If omitted or negative, '
                   'program will run until a SIGINT or SIGTERM is received.')
@click.option('--plot', '-p',
              is_flag=True, default=False, show_default=True,
              help='Plot the resulting CPU load. '
                   'Can only be used with a fixed duration.')
@click.option('--sampling_interval', '-s',
              type=float, default=0.1, show_default=True,
              help='Sampling interval, in seconds, '
                   'for the internal PI controller. '
                   'Changing this value is strongly discouraged!',
              callback=__validate_sampling_interval)
def __main(core, cpu_load, duration, plot, sampling_interval):
    if plot and duration < 0:
        raise click.BadOptionUsage(
            'Plot option can only be used with a fixed duration.')

    if len(cpu_load) > 1 and len(cpu_load) != len(core):
        raise click.BadOptionUsage('Number of cores and loads does not match.')
    elif len(cpu_load) == 1:
        cpu_load = itertools.repeat(cpu_load[0], len(core))

    # filter out repeated core indexes
    core = list(set(core))

    # disable signal handlers before spawning processes
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)

    # spawn one process per core
    with multiprocessing.Pool(len(core)) as pool:
        pool.starmap(load_core, zip(
            core,
            cpu_load,
            itertools.repeat(duration),
            itertools.repeat(plot),
            itertools.repeat(sampling_interval)
        ))


if __name__ == '__main__':
    __main()
