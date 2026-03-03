---
layout: default
title: CPU Load Generator
---

# CPU Load Generator Project

Welcome to the CPU Load Generator project — a Python-based tool that generates a fixed CPU load for a finite or indefinite period on one or more CPU cores, using a **PI controller** (proportional–integral).

![PI Regulator Block Diagram](https://gaetanocarlucci.altervista.org/wp-content/uploads/2024/07/pid-1.png)

## Motivation

This project is ideal for:

- **Performance Testing**  
- **Resource Allocation Optimization**  
- **Benchmarking**  
- **Education & Training**  
- **Thermal & Power Analysis**

## Architecture

The system consists of:

- **CPU Target Load**
- **Monitor Thread** for actual CPU usage measurement
- **Controller Thread** (PI regulator)
- **Actuator** adjusting sleep time for control
- **Disturbances** (e.g., other processes)

## Monitor Thread

Uses `psutil` to sample the **current process** CPU usage (per core when affinity is set):
```python
p = psutil.Process(os.getpid())
sample = p.cpu_percent(sampling_interval)
```

The call blocks for the sampling interval, ensuring timing consistency.

## Controller Thread (PI Regulator)

Calculates a control signal (sleep time) to modulate load. If the error is positive (load too low), it **reduces sleep** to increase load, and vice versa. Tuned experimentally with `kp` and `ki`.

## Actuator

The actuator applies the controller output by alternating CPU-bound work and sleep. Less sleep ⇒ higher load.

```python
def generate_load(self, sleep_time):
    interval = time.time() + self.period - sleep_time
    while time.time() < interval:
        pr = 213123
        _ = pr * pr
        pr += 1
    time.sleep(sleep_time)
```

## Results

The figure below shows the controller maintaining 50% CPU load.

![50% Target CPU Load](https://gaetanocarlucci.altervista.org/wp-content/uploads/2024/07/50-Target-Load.png)

**Supported platforms:** Linux, macOS, and Windows (see [README](https://github.com/GaetanoCarlucci/CPULoadGenerator#readme) for setup). Use `--plot` to show the load curve and save a PNG.

## Resources

- [Source Code on GitHub](https://github.com/GaetanoCarlucci/CPULoadGenerator)
- [Original Article](https://gaetanocarlucci.altervista.org/cpu-load-generator-project/)

---

Thanks for checking out this project! Feel free to contribute or raise issues on the repository.
