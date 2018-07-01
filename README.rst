CPU Load Generator (Python 3)
==============
|travis-badge|_ |mit-badge|_ |made-with-python|_

.. |travis-badge| image:: https://travis-ci.org/GaetanoCarlucci/CPULoadGenerator.svg?branch=master
.. _travis-badge: https://travis-ci.org/GaetanoCarlucci/CPULoadGenerator

.. |mit-badge| image:: https://img.shields.io/:license-mit-green.svg?style=flat
.. _mit-badge: http://opensource.org/licenses/MIT

.. |made-with-python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
.. _made-with-python: https://www.python.org/

This script allows to generate a fixed CPU load for a finite or indefinite time period, for one or more CPU cores.
A PI controller is employed for this purpose.
The script takes in input the desired CPU load and the CPU core on which the load has to be generated.
The controller and the CPU monitor are implemented in two different threads.

Dependencies
-------------

This script uses Python 3.6 and requires the following additional libraries:

- matplotlib
- psutil
- click

To get started, first install Virtualenv, then create and activate a Python virtualenv in the project root directory:

.. code:: bash

    $ cd CPULoadGenerator/
    $ sudo apt install virtualenv
    $ virtualenv --python=python3.6 ./venv
    $ . venv/bin/activate
    (venv) $

Finally, install the dependencies listed in requirements.txt:

.. code:: bash

    (venv) $ pip install -r requirements.txt

Alternatively, install dependencies system-wide using apt:

.. code:: bash

    $ sudo apt install python3-matplotlib python3-psutil python3-click


Examples
-------------
1. Generate 20% of load on core 0 for 20 seconds: ::

    ./CPULoadGenerator.py -l 0.2 -d 20 -c 0

2. Generate 65% load on cores 0, 1 and 5, until the program is interrupted through Ctrl-C: ::

    ./CPULoadGenerator.py -l 0.65 -c 0 -c 1 -c 5

3. Generate 55% load on core 0, 12% on core 3, until the program is interrupted through Ctrl-C: ::

    ./CPULoadGenerator.py -c 0 -c 3 -l 0.55 -l 0.12

4. Generate 12% load on cores 0 and 1, for 20.5 seconds, and then plot the load for each of the cores: ::

    ./CPULoadGenerator.py -l 0.12 -c 0 -c 1 -d 20.5 --plot

5. Example graph of CPU load:

.. image:: https://raw.githubusercontent.com/molguin92/CPULoadGenerator/python3_port_stable/50%25-Target-Load.png
    :alt: Example - 50% load on CPU core 0
    :align: center
