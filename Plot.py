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
        self.line_target, = plt.plot(self.y_target)
        self.line_load, = plt.plot(self.y_load)
        plt.legend([self.line_target, self.line_load], ["Target CPU", "CPU [%d] Load" % (cpu)], ncol=2)
        plt.grid(True)
        self.ts_start = time.time()

    def plotSample(self, sample, target):
        p_x = time.time() - self.ts_start
        p_load = sample
        p_target = target 
        self.y_load.append(p_load)
        self.y_target.append(p_target)
        self.xdata.append(p_x)
        self.line_target.set_xdata(self.xdata)
        self.line_target.set_ydata(self.y_target)
        self.line_load.set_xdata(self.xdata)
        self.line_load.set_ydata(self.y_load)
        plt.draw()

    def close(self):
        plt.savefig("%d %% Load" % (self.cpuT*100) + ".jpg",dpi=100)  
        plt.close();