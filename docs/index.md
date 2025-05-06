---
layout: default
title: CPU Load Generator
---

<a href="https://github.com/GaetanoCarlucci/CPULoadGenerator" style="position: absolute; top: 10px; left: 10px;">GitHub Repo</a>

# CPU Load Generator Project

Welcome to the CPU Load Generator project — a Python-based tool that generates a fixed CPU load for a finite period using a PID regulator.

![PID Regulator Block Diagram](https://gaetanocarlucci.altervista.org/wp-content/uploads/2024/07/pid-1.png)

## 💡 Motivation

This project is ideal for:

- **Performance Testing**  
- **Resource Allocation Optimization**  
- **Benchmarking**  
- **Education & Training**  
- **Thermal & Power Analysis**

## 🧠 Architecture

The system consists of:

- **CPU Target Load**
- **Monitor Thread** for actual CPU usage measurement
- **Controller Thread** (PID regulator)
- **Actuator** adjusting sleep time for control
- **Disturbances** (e.g., other processes)

## 🧪 Monitor Thread

Uses `psutil` to sample CPU load:
```python
psutil.cpu_percent(interval)
```

This blocks the thread for the sampling interval, ensuring timing consistency.

## 🔧 Controller Thread (PID Regulator)

Calculates a control signal to modulate load. If error is positive (load too low), it **reduces sleep** to increase load, and vice versa.

```python
def generate_load(self, sleep_time):
    interval = time.time() + self.period - sleep_time
    while time.time() < interval:
        pr = 213123
        _ = pr * pr
        pr += 1
    time.sleep(sleep_time)
```

Tuned experimentally with `kp` and `ki`.

## 📊 Results

The figure below shows the controller maintaining 50% CPU load.

![50% Target CPU Load](https://gaetanocarlucci.altervista.org/wp-content/uploads/2024/07/50-Target-Load.png)

## 📎 Resources

- [Source Code on GitHub](https://github.com/GaetanoCarlucci/CPULoadGenerator)
- [Original Article](https://gaetanocarlucci.altervista.org/cpu-load-generator-project/)

---

Thanks for checking out this project! Feel free to contribute or raise issues on the repository.
