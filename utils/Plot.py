# Authors: Gaetano Carlucci
#         Giuseppe Cofano

import multiprocessing
import time

import matplotlib

# In child processes (e.g. multiprocessing on macOS) GUI backends often fail:
# set Agg before importing pyplot so the window is not used.
if multiprocessing.current_process().name != 'MainProcess':
    matplotlib.use('Agg')

import matplotlib.pyplot as plt  # noqa: E402  # pylint: disable=import-outside-toplevel


class RealTimePlot:
    """
        Plots the CPU load
    """

    def __init__(self, duration, cpu, target):
        plt.figure()
        plt.axis([0, duration, 0, 100])
        # Only show window in main process; in workers (macOS/multiprocessing) use Agg, no window
        if multiprocessing.current_process().name == 'MainProcess':
            plt.ion()
            plt.show()
        plt.xlabel('Time(sec)')
        plt.ylabel('%')
        self.y_load = [0]
        self.cpuT = target;
        self.y_target = [0]
        self.xdata = [0]
        self.line_load, = plt.plot(self.y_load)
        self.line_target, = plt.plot(self.y_target)
        self.cpu_idx = cpu
        if target != 0:
            plt.legend([self.line_target, self.line_load],
                       ["Target CPU", "CPU [%d] Load" % (cpu)], ncol=2)
        else:
            plt.legend([self.line_load], ["CPU [%d] Load" % (cpu)], ncol=1)
        plt.grid(True)
        self.ts_start = time.time()

    def plot_sample(self, sample, target):
        p_x = time.time() - self.ts_start
        p_load = sample
        self.xdata.append(p_x)
        if target != 0:
            p_target = target
            self.y_target.append(p_target)
            self.line_target.set_xdata(self.xdata)
            self.line_target.set_ydata(self.y_target)
        self.y_load.append(p_load)
        self.line_load.set_xdata(self.xdata)
        self.line_load.set_ydata(self.y_load)
        plt.draw()
        # Run GUI event loop so the window updates in real time (main process only)
        if multiprocessing.current_process().name == 'MainProcess':
            plt.pause(0.01)

    def close(self):
        if self.cpuT != 0:
            # self.cpuT is already in 0-100 (passed as get_cpu_target() * 100)
            name = f'{int(round(self.cpuT))}%-Target-Load' \
                   f'-CPU{self.cpu_idx}.png'
            # TODO: add option to change format
            plt.savefig(name, dpi=100)
            # When using Agg (no window), inform user where the plot was saved
            if multiprocessing.current_process().name != 'MainProcess':
                import os
                print(f'Plot saved to: {os.path.abspath(name)}')
        plt.close()
