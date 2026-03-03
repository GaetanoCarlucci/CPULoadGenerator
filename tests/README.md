# Review: tests in the `tests/` folder

## Overview

| File | Purpose | CI |
|------|--------|-----|
| **PID.py** | PI controller closed-loop test: CPU target sequence, save dynamics, PNG plots | ✅ run |
| **feedForward.py** | Open-loop test: sleep time sequence (CPU model), comparison with monitor | ✅ run |
| **Identification.py** | Identification: for each sleep time estimates mean CPU load, scatter plot sleep vs load | ❌ not in CI |
| **Identification2.py** | Alternative identification: sleep time sequence, dynamics plot and PNG | ❌ not in CI |

---

## Strengths

- **Component reuse:** Monitor, Controller, ClosedLoopActuator, OpenLoopActuator used consistently.
- **Reproducibility:** `testing = 1` runs the experiment, `testing = 0` loads data from JSON files (useful to regenerate plots without re-running).
- **CI:** PID and feedForward are run on push/PR (Python 3.9 and 3.13).

---

## Issues and risks

### 1. ~~**macOS / cross-platform compatibility**~~ (fixed)

- **PID.py** and **feedForward.py** import `_available_cores` from `cpu_load_generator` (same logic as main script) → they work on macOS too.

### 2. ~~**Use of `monitor.running` (bug)**~~ (fixed)

- In **Identification.py** and **Identification2.py**, `monitor.running = 0` was replaced with **`monitor.stop()`** before `monitor.join()`.

### 3. ~~**Duplicate `monitor.join()` in Identification.py**~~ (fixed)

- Removed the redundant second `monitor.join()`; a single `monitor.stop()` + `monitor.join()`.

### 4. **Path and imports**

- All tests use `sys.path.insert(0, ...)` to import from the parent. This works when run from repo root; from `tests/` it may depend on cwd.
- CI runs from repo root (`python tests/PID.py`), so it is fine. Running from `tests/` might not find `utils`.
- Optional: use `python -m tests.PID` from root, or document “run from project root”.

### 5. **Files and figures written to cwd**

- Tests write `pid_data`, `feed_forward_data`, `identification_data`, `scatter_plot_data`, and PNGs (`PID.png`, `FeedForward.png`, `Identification.png`, etc.) to the **current working directory**.
- In CI the cwd is the repo root → these files end up in the repo and could be committed by mistake (though `.gitignore` has `*.png`).
- **Suggestion:** write to a subfolder (e.g. `tests/output/` or `tests/artifacts/`) and add it to `.gitignore`, or use `tempfile.gettempdir()`.

### 6. **No assertions**

- The tests do **not** use `assert` or a framework (pytest/unittest). They only check that the run does not crash and produce data/plots.
- Useful as characterization/identification scripts; less so as automated tests (e.g. “controller reaches target within X seconds”).
- Optional: add minimal checks (e.g. `assert len(dynamics['cpu']) > 0`, or thresholds on mean error) to make CI tests more robust.

### 7. **Identification and Identification2 not in CI**

- **Identification.py** and **Identification2.py** are not run by the CI workflow. If something breaks in Monitor/OpenLoopActuator, CI won’t catch it for these two.
- **Suggestion:** include them in CI (at least as “run without crash”) or document that they are manual identification scripts.

### 8. **Unused variables**

- `dynamics_plot_online` is defined but not clearly used to change behaviour (in some places it is only passed to OpenLoopActuator as `plot`). It can be removed or used explicitly.

### 9. **Axis labels and titles**

- In several places the x-axis is labeled "Time [ms]" while the dynamics use `time.time()` (seconds). It should be "Time [s]" for consistency.

---

## Recommended actions summary

| Priority | Action |
|----------|--------|
| ~~High~~ | ~~Make PID.py and feedForward.py macOS-compatible~~ (done: `_available_cores` from `cpu_load_generator`). |
| ~~High~~ | ~~Replace `monitor.running = 0` with `monitor.stop()`~~ (done in Identification and Identification2). |
| Medium | Write data and PNGs to `tests/output/` (or similar) and add to `.gitignore`. |
| Medium | Fix "Time [ms]" → "Time [s]" where data are in seconds. |
| Low | Add Identification.py and Identification2.py to CI (at least as smoke). |
| Low | Add some asserts or pytest to turn them into proper automated tests. |

---

## How to run the tests

From the **project root**:

```bash
pip install -r requirements.txt
python tests/PID.py
python tests/feedForward.py
python tests/Identification.py   # optional, may open windows
python tests/Identification2.py
```

The tests are aligned with the main script changes (`cpu_load_generator.py`, cross-platform cores, monitor stop).
