import psutil
from threading import Thread, Event


class MonitorThread(Thread):
    """Monitors the CPU status.

    param cpu_core: the number of logical core to monitor
    type cpu_core: int
    param interval: sampling interval
    type interval: float
    """

    def __init__(self, cpu_core, sampling_interval=0.1):
        super(MonitorThread, self).__init__()

        self._cpu_core = cpu_core
        self._sampling_interval = sampling_interval

        self.current_cpu_load = 0.0
        self.running = Event()

    def run(self):
        """Start and run the monitor thread."""
        self.running.set()

        while self.running.is_set():
            sample = psutil.cpu_percent(interval=self._sampling_interval, percpu=True)[self._cpu_core]
            self.current_cpu_load = sample
