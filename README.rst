CPULoadGenerator
================

This simple script allows to generate a fixed CPU load for a finite time period. To the purpose, a PI controller is employed. 
The script takes the desired CPU load and the duration of the load generation as input. The process is forced to run only on CPU 0. The controller and the CPU monitor are implemented in two different threads.


Usage
-------------
To run it for "duration" in seconds at the setpoint in % of CPU utilization: ::
	
	./CpuLoadGenerator.py -l <setpoint> -d <duration>
