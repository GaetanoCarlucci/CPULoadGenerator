import multiprocessing as mp

from cpu_load_generator.common._monitor import MonitorThread
from cpu_load_generator.common._controller import ControllerThread
from cpu_load_generator.common._closed_loop_actuator import ClosedLoopActuator


def load_single_core(core_num, duration, load):
    monitor = MonitorThread(core_num)
    monitor.start()

    control = ControllerThread(load)
    control.start()

    actuator = ClosedLoopActuator(control, monitor, duration, core_num, load)
    actuator.run()

    monitor.running.clear()
    control.running.clear()


def load_all_cores(duration, load):
    processes = []
    for core_num in range(mp.cpu_count()):
        process = mp.Process(target=load_single_core, args=(core_num, duration, load))
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()