# Memory Monitor (Project 008)

A real-time monitoring utility that tracks the RAM usage of specific processes to detect anomalies, resource exhaustion, and potential stability failure points.

## Technical Explanation

* **Stateful Process Handle Caching:** Uses a customized lazy-loading fetch routine (`_fetch_process_instance`) to find and cache the `psutil.Process` object. This eliminates the massive CPU overhead caused by scanning the entire kernel process tree (`psutil.process_iter`) on every cycle.
* **RSS Metric Extraction:** Focuses strictly on Resident Set Size (RSS), which isolates the actual, physical portion of memory held by the process inside the hardware RAM, filtering out deceptive virtual memory values.
* **Memory Crash Guards:** Evaluates active process bounds inside a fault-tolerant monitoring loop. If a targeted process terminates or drops handle privileges, the engine safely resets the cache and initializes a non-blocking re-scan.
* **Modernized Byte Scale Math:** Converts raw system bytes to Megabytes utilizing Python's exponential power operator (`1024 ** 2`), aligning the script with modern sênior mathematical data formatting conventions.

## Problems Solved

* **Resource Drainage Evasion:** Instantly isolates rogue processes or memory leaks before they exhaust the host machine's physical hardware capacity, preventing total operating system freezes.
* **Cryptojacking & Shell Telemetry:** Flags hidden threat spikes (such as background file compression or malicious staging execution) that dynamically abuse system thresholds.
* **Automated Baseline Verification:** Allows infrastructure engineers to monitor and establish standard consumption metrics for business-critical operational tasks.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Lookup Strategy** | Process Handle Cache | Scanning the process tree repeatedly spikes CPU usage. Caching the active process pointer drops utility overhead to near zero. |
| **Volatile Metric** | RSS (Resident Set Size) | Virtual memory allocations include swapped disk files and shared pages, making RSS the only accurate representation of actual RAM footprint. |
| **Math Structure** | Exponential Scaling (`1024 ** 2`) | Cleaner and more modern than flat multiplication values (`1024 * 1024`), optimizing numerical data type readability. |
| **Execution Loop** | CLI Arguments Engine | Bypasses restrictive user prompts (`input()`), making the script instantly compatible with headless infrastructure and multi-process automation tasks. |

## Usage

This utility features a modern, parameter-driven terminal interface. Execute the application by passing the target process name and the optional memory threshold (in MB) directly as arguments:

```bash
# Monitor a process using the default 100MB threshold
python memory_monitor.py chrome

# Monitor a process with an explicit 350MB alert limit
python memory_monitor.py slack 350.0
