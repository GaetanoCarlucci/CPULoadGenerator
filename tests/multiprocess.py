import multiprocessing as mp

import psutil

from cpu_load_generator.utils.Monitor import MonitorThread
from cpu_load_generator.utils.Controller import ControllerThread
from cpu_load_generator.utils.closedLoopActuator import closedLoopActuator


def burn_cpu(cpu_num, load_level, duration):
    psutil.Process().cpu_affinity([cpu_num])

    monitor = MonitorThread(cpu_num, 0.1)
    monitor.start()

    control = ControllerThread(0.1)
    control.start()
    control.setCpuTarget(load_level)

    actuator = closedLoopActuator(control, monitor, duration, cpu_num, load_level, False)
    actuator.run()
    actuator.close()

    monitor.running = 0
    control.running = 0
    monitor.join()
    control.join()


if __name__ == '__main__':
    cpu_count = mp.cpu_count()
    cpu_load = 0.5
    load_duration = 20

    processes = []
    for cpu_id in range(cpu_count):
        process = mp.Process(target=burn_cpu, args=(cpu_id, cpu_load, load_duration))
        processes.append(process)
        process.start()

    for p in processes:
        p.join()
