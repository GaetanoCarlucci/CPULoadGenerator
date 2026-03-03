# CPU Load Generator

[![CI](https://img.shields.io/github/actions/workflow/status/GaetanoCarlucci/CPULoadGenerator/ci.yml)](https://github.com/GaetanoCarlucci/CPULoadGenerator/actions)
[![License: MIT](https://img.shields.io/:license-mit-green.svg?style=flat)](http://opensource.org/licenses/MIT)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

This script generates a fixed CPU load for a finite or indefinite time period, on one or more CPU cores. A **PI controller** is used for this purpose.

You provide the desired CPU load and the CPU core(s) to load. The controller and the CPU monitor run in separate threads.

**Supported platforms:** Linux, macOS, and Windows (Windows is less tested; `psutil` supports CPU affinity on all three).

## Theoretical insight

- **Project homepage:** [https://gaetanocarlucci.github.io/CPULoadGenerator/](https://gaetanocarlucci.github.io/CPULoadGenerator/) — more details on the tool.
- **Blog:** [Theoretical explanation of this tool](https://gaetanocarlucci.altervista.org/cpu-load-generator-project/).

## Dependencies

- **Python 3.6+**
- **Libraries:** `matplotlib`, `psutil`, `click`

### Setup with virtualenv

```bash
cd CPULoadGenerator/
sudo apt install virtualenv
virtualenv --python=python3.6 ./venv
. venv/bin/activate
(venv) $ pip install -r requirements.txt
```

### System-wide install (Debian/Ubuntu)

```bash
sudo apt install python3-matplotlib python3-psutil python3-click
```

### Run on macOS

1. Create and activate a virtual environment (recommended):

   ```bash
   cd CPULoadGenerator/
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the script (e.g. 20% load on core 0 for 10 seconds):

   ```bash
   python CPULoadGenerator.py -l 0.2 -d 10 -c 0
   ```

   Or make it executable and run: `chmod +x CPULoadGenerator.py` then `./CPULoadGenerator.py -l 0.2 -d 10 -c 0`.

**Note for macOS:** CPU affinity (pinning a process to a specific core) is not supported by the OS, so the process is not bound to the chosen core. The script still generates the requested load; it may just be distributed across cores by the scheduler. All other behaviour (PI control, duration) is unchanged.

With `--plot`: use **exactly one core** to see the **live plot window** on macOS (e.g. `-c 0 -l 0.5 -d 20 --plot`). With multiple cores, the plot is saved to a PNG file at the end. If the window does not appear or stays blank, try `export MPLBACKEND=TkAgg` before running, or install a GUI backend: `pip install pyobjc-framework-Cocoa` (for the default macOS backend).

## Examples

1. **20% load on core 0 for 20 seconds:**

   ```bash
   ./CPULoadGenerator.py -l 0.2 -d 20 -c 0
   ```

2. **65% load on cores 0, 1 and 5, until interrupted (Ctrl-C):**

   ```bash
   ./CPULoadGenerator.py -l 0.65 -c 0 -c 1 -c 5
   ```

3. **55% load on core 0, 12% on core 3, until interrupted:**

   ```bash
   ./CPULoadGenerator.py -c 0 -c 3 -l 0.55 -l 0.12
   ```

4. **12% load on cores 0 and 1 for 20.5 seconds, then plot the load:**

   ```bash
   ./CPULoadGenerator.py -l 0.12 -c 0 -c 1 -d 20.5 --plot
   ```

5. **Example graph of CPU load (50% target on core 0):**

   ![Example - 50% load on CPU core 0](https://raw.githubusercontent.com/molguin92/CPULoadGenerator/python3_port_stable/50%25-Target-Load.png)
