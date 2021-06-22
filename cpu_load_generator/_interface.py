import multiprocessing as mp
import os
import psutil
import json

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


def from_profile(path_to_profile_json):
    """Run CPU loader from a profile.

    param path_to_profile_json: path to profile file
    type path_to_profile_json: str

    """

    profile = _read_profile(path_to_profile_json)

    processes = []
    for single_sequence in profile:
        process = mp.Process(target=_run_single_sequence,
                             args=(single_sequence["cpu_num"], single_sequence["repeat"], single_sequence["sequence"]))
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()


def _run_single_sequence(core_num, repeat, sequence):
    """Load single logical core.

    param core_num: number of the core on which the load will be put
    type core_num: int
    param repeat: number of iterations a single profile will be run
    type repeat: int
    param sequence: single profile sequence
    type repeat: dict

    """

    process = psutil.Process(os.getpid())
    process.cpu_affinity([core_num])

    monitor = MonitorThread(core_num)
    monitor.start()

    control = ControllerThread(target_cpu_load=0.01)
    control.start()

    actuator = ClosedLoopActuator(controller=control, monitor=monitor, duration_s=0.0,
                                  cpu_core_num=core_num, cpu_target=0.0)

    for _ in range(repeat):
        for single_profile in sequence:
            target_load = single_profile['load']
            duration_s = single_profile['duration_s']

            control.target_cpu_load = target_load
            actuator.duration_s = duration_s
            actuator.cpu_target = target_load
            actuator.run()

    monitor.running.clear()
    control.running.clear()


def _read_profile(path_to_profile_json):
    """Read json CPU load profile file.

    param path_to_profile_json: path to CPU load profile json file
    type: str
    returns: deserialized CPU load profile sequence

    """

    with open(path_to_profile_json, "r") as json_file:
        sequence = json.load(json_file)

    return sequence
