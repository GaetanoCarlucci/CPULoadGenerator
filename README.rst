CPULoadGenerator
================
|travis-badge|_

.. |travis-badge| image:: https://travis-ci.org/GaetanoCarlucci/CPULoadGenerator.svg?branch=master
.. _travis-badge: https://travis-ci.org/GaetanoCarlucci/CPULoadGenerator

This script allows to generate a fixed CPU load for a finite time period. To the purpose, a PI controller is employed. 
The script takes in input the desired CPU load, the duration of the experiment, the cpu core on which generate the load.  The controller and the CPU monitor are implemented in two different threads.

Dependencies
-------------
Install matplotlib for real time plot of CPU status: ::

	sudo apt-get install python-matplotlib

Install psutil: ::

	sudo apt-get install python-psutil

Usage
-------------
To generate 20% of load on core 0 for 20 seconds run: :: 
	
	./CpuLoadGenerator.py -l 0.2 -d 20 -c 0

To enable real time plot run: :: 
	
	./CpuLoadGenerator.py -p 1
	
To generate 20% of CPU load on core 0 and on core 1 run: :: 
	
	./CpuLoadGenerator.py -c 1 -l 0.2 | ./CpuLoadGenerator.py -c 0 -l 0.2

Example
-------------
Dynamics example: 50% load generated on CPU core 0: ::
	
	./CPULoadGenerator.py -l 0.5 -d 20 -p 1

.. image:: https://raw.githubusercontent.com/GaetanoCarlucci/CPULoadGenerator/master/50%25-Target-Load.jpg
    :alt: Example - 50% load on CPU core 0
    :align: center
