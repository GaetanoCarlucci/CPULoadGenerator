#Authors: Gaetano Carlucci
#         Giuseppe Cofano

import time
import matplotlib.pyplot as plt

class realTimePlot():
    """
        Plots the CPU load
    """
    def __init__(self, duration, cpu, target):
        plt.figure()
        plt.axis([0, duration, 0, 100])
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
        if target != 0:
            plt.legend([self.line_target, self.line_load], ["Target CPU", "CPU [%d] Load" % (cpu)], ncol=2)
        else:
            plt.legend([self.line_load], ["CPU [%d] Load" % (cpu)], ncol=1)
        plt.grid(True)
        self.ts_start = time.time()

    def plotSample(self, sample, target):
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

    def close(self):
        if self.cpuT != 0:
            name = "%d%%-Target-Load" % (self.cpuT*100)+ ".png"
            plt.savefig(name, dpi=100)
        plt.close();