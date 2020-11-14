import multiprocessing as mp
import os

import psutil

from cpu_load_generator.common._monitor import MonitorThread
from cpu_load_generator.common._controller import ControllerThread
from cpu_load_generator.common._closed_loop_actuator \
    import ClosedLoopActuator


def load_single_core(core_num, duration_s, target_load):
    """Load single logical core.

    param core_num: number of CPU core to put some load on
    type core_num: int
    param duration_s: time period in seconds in which the CPU core will be loaded.
    type duration_s: int, float
    param target_load: CPU load level in fractions of 1
    type target_load: float

    """
    process = psutil.Process(os.getpid())
    process.cpu_affinity([core_num])

    monitor = MonitorThread(core_num)
    monitor.start()

    control = ControllerThread(target_load)
    control.start()

    actuator = ClosedLoopActuator(control, monitor, duration_s, core_num, target_load)
    actuator.run()

    monitor.running.clear()
    control.running.clear()


def load_all_cores(duration_s, target_load):
    """Load all available logical cores.

    param duration_s: time period in seconds in which the CPU core will be loaded.
    type duration_s: int, float
    param target_load: CPU load level in fractions of 1
    type target_load: float

    """

    processes = []
    for core_num in range(mp.cpu_count()):
        process = mp.Process(target=load_single_core, args=(core_num, duration_s, target_load))
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()
