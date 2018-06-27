#!/usr/bin/env python

# Authors: Gaetano Carlucci
#         Giuseppe Cofano
# Python3 port: Manuel Olguín
import itertools
import multiprocessing
import signal

import click

from utils.ClosedLoopActuator import ClosedLoopActuator
from utils.Controller import ControllerThread
from utils.Monitor import MonitorThread


# sys.path.insert(0, 'utils')

class ShutdownException(Exception):
    pass


def __sig_handler(*args):
    raise ShutdownException()


def __validate_cpu_load(ctx, param, value):
    if not 0. <= value <= 1.:
        raise click.BadOptionUsage('CPU load out of range [0, 1]')
    return value


def load_core(target_load, target_core, duration_seconds=-1, plot=False):
    if duration_seconds >= 0:
        print(f'Loading core {target_core} ({target_load * 100.0}%) for '
              f'{duration_seconds} seconds.')
    else:
        print(f'Loading core {target_core} ({target_load * 100.0}%) until '
              f'interrupted.')

    monitor = MonitorThread(target_core, 0.1)
    control = ControllerThread(0.1)
    control.set_cpu_target(target_load)
    actuator = ClosedLoopActuator(control, monitor, duration_seconds,
                                  target_core, target_load, plot)

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


@click.command()
@click.option('--cpu_load', '-l', type=float, help='Target CPU load',
              default=0.2, show_default=True, callback=__validate_cpu_load)
@click.option('--core', '-c',
              type=click.IntRange(0, multiprocessing.cpu_count() - 1),
              required=True, multiple=True,
              help='CPU core to artificially load. '
                   'Can be specified multiple times to load multiple cores.')
@click.option('--duration', '-d', type=float, default=-1, show_default=True,
              help='Duration in seconds. If omitted or negative, '
                   'program will run until a SIGINT or SIGTERM is received.')
@click.option('--plot', '-p', is_flag=True, default=False, show_default=True,
              help='Plot the resulting CPU load. '
                   'Can only be used with a fixed duration.')
def __main(cpu_load, core, duration, plot):
    if plot and duration < 0:
        raise click.BadOptionUsage(
            'Plot option can only be used with a fixed duration.')

    # filter out repeated core indexes
    core = list(set(core))

    # disable signal handlers before spawning processes
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)

    # spawn one process per core
    with multiprocessing.Pool(len(core)) as pool:
        pool.starmap(load_core, zip(
            itertools.repeat(cpu_load),
            core,
            itertools.repeat(duration),
            itertools.repeat(plot)
        ))


if __name__ == '__main__':
    __main()
