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

@click.option('--frequency', '-f',
              type=int, default=-1, show_default=True,
              help='Control cpu p-state by setting cpu frequency'
              '-1: no change, 0: defalut p-state,1: min, 2: middle, 3: max'
                   )



def __main(core, cpu_load, duration, plot, sampling_interval,frequency):
    if plot and duration < 0:
        raise click.BadOptionUsage(
            'Plot option can only be used with a fixed duration.')

    if len(cpu_load) > 1 and len(cpu_load) != len(core):
        raise click.BadOptionUsage('Number of cores and loads does not match.')
    elif len(cpu_load) == 1:
        cpu_load = itertools.repeat(cpu_load[0], len(core))
        
    """
    apt-get install cpufrequtils
    要设置CPU频率，您可以使用以下命令格式：
    ```
    sudo cpufreq-set -c <CPU编号> -u <最大频率> -d <最小频率> -g <性能模式>
    
    sudo cpufreq-set -c 0 -d 1400000 -u 1800000 -g performance
    ```

    其中，-c参数用于指定CPU编号，如果您的系统只有一个CPU，可以忽略此参数；-f参数用于指定最大频率，单位是千赫兹；-u参数用于指定最小频率；-g参数用于指定性能模式，您可以选择以下其中一个：

    - performance：最高性能模式
    - powersave：最低功耗模式
    - ondemand：根据使用情况动态调整频率
    - conservative：类似于ondemand，但尽可能在较低频率下运行以节省更多功耗

    例如，如果您要将CPU最大频率设置为2.5 GHz，最小频率设置为1 GHz，性能模式设置为powersave，可以使用以下命令：

    ```
    sudo cpufreq-set -f 2500000 -u 1000000 -g powersave
    ```

    需要注意的是，这只是临时设置，重启系统后会失效。如果您想让设置永久生效，需要编辑CPU频率配置文件，在其中添加类似上面命令的配置。
    """
    if frequency==-1:
        all_ava_freq = os.popen("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies").readlines()[0].replace('\n','')
        curr_freq = os.popen("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq").readlines()[0].replace('\n','')
        print(f"all avaliable frequency: {all_ava_freq}\ncurrent cpu frequency: {curr_freq}")
    elif frequency==0:
        res = os.popen("cpufreq-set -r").readlines()[0].replace('\n','')
        print(res)
    elif frequency==1:
        min_freq = os.popen("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies | awk '{print $NF}'").readlines()[0].replace('\n','')
        print(f"set min cpu frequency {min_freq}")
        res = os.popen(f'cpufreq-set -f {min_freq}').readlines()
        print(res)
    elif frequency==2:
        middle_freq = os.popen("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies | awk '{print $2}'").readlines()[0].replace('\n','')
        print(f"set middle cpu frequency {middle_freq}")
        res = os.popen(f'cpufreq-set -f {middle_freq}').readlines()
        print(res)
    elif frequency==3:
        max_freq = os.popen("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies | awk '{print $1}'").readlines()[0].replace('\n','')
        print(f"set max cpu frequency {max_freq}")
        res = os.popen(f'cpufreq-set -f {max_freq}').readlines()
        print(res)
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
