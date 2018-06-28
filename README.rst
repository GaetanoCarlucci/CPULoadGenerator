CPU Load Generator (Python 2)
================
|travis-badge|_ |mit-badge|_ |made-with-python|_

.. |travis-badge| image:: https://travis-ci.org/GaetanoCarlucci/CPULoadGenerator.svg?branch=master
.. _travis-badge: https://travis-ci.org/GaetanoCarlucci/CPULoadGenerator

.. |mit-badge| image:: https://img.shields.io/:license-mit-green.svg?style=flat
.. _mit-badge: http://opensource.org/licenses/MIT

.. |made-with-python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
.. _made-with-python: https://www.python.org/


This script allows to generate a fixed CPU load for a finite time period. To the purpose, a PI controller is employed. 
The script takes in input the desired CPU load, the duration of the experiment and the CPU core on which the load has to be generated. The controller and the CPU monitor are implemented in two different threads.

Python versions
**********************
This master branch refers to Python versions **2.7, 3.2, 3.3, 3.4**.

`Here <https://github.com/GaetanoCarlucci/CPULoadGenerator/tree/Python3/>`_ it is the **3.6** version branch which contains some extended features.

Dependencies
**********************
Install matplotlib for real time plot of CPU status: ::

	sudo apt-get install python-matplotlib

Install psutil: ::

	sudo apt-get install python-psutil
	
Other dependencies: ::

        sudo apt-get install python-twisted

Usage
**********************
To generate 20% of load on core 0 for 20 seconds run: :: 
	
	./CPULoadGenerator.py -l 0.2 -d 20 -c 0

To enable real time plot run: :: 
	
	./CPULoadGenerator.py -p 1
	
To generate 20% of CPU load on core 0 and on core 1 run: :: 
	
	./CPULoadGenerator.py -c 1 -l 0.2 | ./CPULoadGenerator.py -c 0 -l 0.2

Example
**********************
Dynamics example: 50% load generated on CPU core 0: ::
	
	./CPULoadGenerator.py -l 0.5 -d 20 -p 1

.. image:: https://raw.githubusercontent.com/GaetanoCarlucci/CPULoadGenerator/master/50%25-Target-Load.jpg
    :alt: Example - 50% load on CPU core 0
    :align: center
