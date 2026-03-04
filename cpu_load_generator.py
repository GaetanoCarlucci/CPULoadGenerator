#!/usr/bin/env python
"""Generate a fixed CPU load on one or more cores using a PI controller."""

# Authors: Gaetano Carlucci
#         Giuseppe Cofano
# Python3 port: Manuel Olguín
import argparse
import itertools
import multiprocessing
import os
import signal
import sys
import psutil

from utils.ClosedLoopActuator import ClosedLoopActuator, \
    PlottingClosedLoopActuator
from utils.Controller import ControllerThread
from utils.Monitor import MonitorThread


def _available_cores():
    """Return list of available CPU core indices. Works on Linux, macOS, and Windows."""
    try:
        p = psutil.Process(os.getpid())
        return list(p.cpu_affinity())
    except (AttributeError, psutil.AccessDenied):
        return list(range(psutil.cpu_count()))


def _set_cpu_affinity(core_id):
    """Pin process to a CPU core if the platform supports it (Linux, Windows). No-op on macOS."""
    try:
        process = psutil.Process(os.getpid())
        process.cpu_affinity([core_id])
    except (AttributeError, psutil.AccessDenied):
        pass


class ShutdownException(Exception):
    """Raised on SIGINT/SIGTERM to trigger graceful shutdown of load generation."""


def __sig_handler(*args):
    raise ShutdownException()


def load_core(target_core, target_load,
              duration_seconds=-1, plot=False,
              sampling_interval=0.1):
    """Run the PI-controlled load generator on a single CPU core."""
    if duration_seconds >= 0:
        print(f'Loading core {target_core} ({target_load * 100.0:0>5.2f}%) for '
              f'{duration_seconds} seconds.')
    else:
        print(f'Loading core {target_core} ({target_load * 100.0:0>5.2f}%) '
              f'until interrupted.')

    if sampling_interval <= 0:
        raise ValueError('Negative sampling interval!')
    # Lock this process to the target core (no-op on macOS; load still applied)
    _set_cpu_affinity(target_core)

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


def _parse_args():
    """Parse command-line arguments. Exits on validation errors."""
    available = _available_cores()
    p = argparse.ArgumentParser(
        description='Generate a fixed CPU load on one or more cores (PI controller).'
    )
    p.add_argument(
        '--core', '-c', type=int, nargs='*', default=available,
        metavar='N',
        help=f'CPU core(s) to load (default: all: {available})'
    )
    p.add_argument(
        '--cpu_load', '-l', type=float, nargs='*', default=[0.2],
        metavar='L',
        help='Target load per core in [0, 1]; one value for all cores (default: 0.2)'
    )
    p.add_argument(
        '--duration', '-d', type=float, default=-1,
        help='Duration in seconds; negative = until SIGINT/SIGTERM (default: -1)'
    )
    p.add_argument(
        '--plot', '-p', action='store_true',
        help='Plot CPU load and save a PNG (single core, fixed duration only)'
    )
    p.add_argument(
        '--sampling_interval', '-s', type=float, default=0.1,
        help='PI controller sampling interval in seconds (default: 0.1)'
    )
    args = p.parse_args()

    core = args.core if args.core else available
    cpu_load = args.cpu_load if args.cpu_load else [0.2]

    for v in core:
        if v not in available:
            sys.exit(f'Target core {v} is not in available cores: {available}')
    for v in cpu_load:
        if not 0. <= v <= 1.:
            sys.exit(f'CPU load {v} out of range [0, 1]')
    if args.sampling_interval < 0:
        sys.exit(f'Sampling interval cannot be negative ({args.sampling_interval})')
    if args.plot and args.duration < 0:
        sys.exit('Plot option requires a fixed duration (use -d SECONDS).')
    if len(cpu_load) > 1 and len(cpu_load) != len(core):
        sys.exit('Number of cores and loads must match when specifying multiple loads.')

    return core, cpu_load, args.duration, args.plot, args.sampling_interval


def _main() -> None:
    """Entry point: parse CLI, then run load on selected core(s)."""
    core, cpu_load, duration, plot, sampling_interval = _parse_args()
    if len(cpu_load) == 1:
        cpu_load = itertools.repeat(cpu_load[0], len(core))

    # filter out repeated core indexes
    core = list(set(core))

    # Plot only makes sense for a single core; ignore -p when running on multiple/all cores
    if plot and len(core) > 1:
        print('Plot disabled when using multiple cores (use -c 0 for single-core plot).')
        plot = False

    # Single core + plot: run in main process so the live plot window works
    if len(core) == 1 and plot:
        load_core(core[0], next(cpu_load), duration, plot, sampling_interval)
        return

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
    _main()
