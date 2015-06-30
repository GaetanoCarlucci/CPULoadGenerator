CPULoadGenerator
================

This simple script allows to generate a fixed CPU load for a finite time period. To the purpose, a PI controller is employed. 
The script takes the desired CPU load and the duration of the load generation as input. The process is forced to run only on CPU 0. The controller and the CPU monitor are implemented in two different threads.


Usage
-------------
Install matplotlib: it allows to monitor the status of CPU 0: ::

	sudo apt-get install python-matplotlib

To run the script that generates CPU load run: :: 
	
	./CpuLoadGenerator.py -l <setpoint> -d <duration>

where **duration** sets the time duration of the script in seconds and **setpoint** sets the percentage of CPU load to generate.