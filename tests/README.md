# Tests

## What runs in CI

On every push and pull request to `master`, the [CI workflow](../.github/workflows/ci.yml) runs:

- **Python 3.13** on Ubuntu
- After `pip install -r requirements.txt`:
  - `python tests/PID.py`
  - `python tests/feedForward.py`

If both scripts complete without errors, the build passes. They produce data files and PNGs in the current working directory (repo root when run from CI).

## Scripts

| Script | Run in CI | Description |
|--------|-----------|-------------|
| **PID.py** | Yes | Closed-loop (PI) test: runs a sequence of CPU targets, records dynamics, saves `pid_data` and PNGs (e.g. `PID.png`, `PID Actuation.png`). |
| **feedForward.py** | Yes | Open-loop test: runs a sequence of sleep times, records dynamics, saves `feed_forward_data` and `FeedForward.png`. |
| **Identification.py** | No | Identification script: sweep sleep times, estimate CPU load, scatter plots. Run manually from project root if needed. |
| **Identification2.py** | No | Alternative identification: sleep-time sequence and dynamics plot. Run manually from project root if needed. |

## How to run (same as CI)

From the **project root**:

```bash
pip install -r requirements.txt
python tests/PID.py
python tests/feedForward.py
```

Run from the project root so imports (`utils`, `cpu_load_generator`) resolve correctly.
