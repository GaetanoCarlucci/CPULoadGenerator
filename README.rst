CPU Load Generator
================
|travis-badge|_ |mit-badge|_

.. |travis-badge| image:: https://travis-ci.org/GaetanoCarlucci/CPULoadGenerator.svg?branch=master
.. _travis-badge: https://travis-ci.org/GaetanoCarlucci/CPULoadGenerator

.. |mit-badge| image:: https://img.shields.io/:license-mit-green.svg?style=flat
.. _mit-badge: http://opensource.org/licenses/MIT

This script allows to generate a fixed CPU load for a finite time period. To the purpose, a PI controller is employed. 
The script takes in input the desired CPU load, the duration of the experiment and the CPU core on which the load has to be generated. The controller and the CPU monitor are implemented in two different threads.

Dependencies
-------------

This script uses Python 3.6 and requires the following additional libraries:

- matplotlib
- psutil
- twisted

To get started, first install the virtualenv, then create and activate a Python virtualenv in the project root directory: .. highlight:: bash

    $ cd CPULoadGenerator/
    $ sudo apt install virtualenv
    $ virtualenv --python=python3.6 ./venv
    $ . venv/bin/activate
    (venv) $

Finally, install the dependencies listed in requirements.txt: .. highlight:: bash

    (venv) $ pip install -r requirements.txt

Alternatively, install dependencies system-wide using apt: .. highlight:: bash

    $ sudo apt install python3-matplotlib python3-psutil python3-twisted


Usage
-------------
To generate 20% of load on core 0 for 20 seconds run: :: 
	
	./CPULoadGenerator.py -l 0.2 -d 20 -c 0

To enable real time plot run: :: 
	
	./CPULoadGenerator.py -p 1
	
To generate 20% of CPU load on core 0 and on core 1 run: :: 
	
	./CPULoadGenerator.py -c 1 -l 0.2 | ./CPULoadGenerator.py -c 0 -l 0.2

Example
-------------
Dynamics example: 50% load generated on CPU core 0: ::
	
	./CPULoadGenerator.py -l 0.5 -d 20 -p 1

.. image:: https://raw.githubusercontent.com/GaetanoCarlucci/CPULoadGenerator/master/50%25-Target-Load.jpg
    :alt: Example - 50% load on CPU core 0
    :align: center
