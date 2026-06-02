# Memory Monitor (Project 008)

A real-time monitoring utility that tracks the RAM usage of specific
processes to detect anomalies and resource exhaustion.

## Technical Explanation

-   **Process Iteration:** Utilizes *psutil.process_iter* to dynamically
    query the OS process table for memory metrics.
-   **RSS Calculation:** Focuses on RSS (Resident Set Size), which
    accurately represents the portion of memory occupied by a process in
    physical RAM.
-   **Non-blocking Loop:** Runs a simple *while* loop with *time.sleep*
    to minimize CPU footprint during monitoring.

## Problems Solved

1.  **Malware Detection:** Sudden memory spikes can indicate malicious
    activities, such as data encryption or automated exfiltration
    processes.
2.  **Performance Troubleshooting:** Helps identify processes causing
    system-wide instability.
3.  **Automated Baselining:** Allows security analysts to establish
    normal memory usage patterns for critical business processes.

## Design Decisions: \"Why this instead of that?\"

  ------------ -------------------------- ----------------------------------------------------------------------------------------------------------
  **Metric**   RSS (Resident Set Size)    Most accurate metric for physical RAM usage, unlike virtual memory which can be misleading.
  **Search**   *target.lower() in name*   Provides case-insensitive matching, ensuring the monitor works regardless of how the process is written.
  **Loop**     *while True* + *sleep*     Simple, robust, and provides low overhead for continuous monitoring tasks.
  ------------ -------------------------- ----------------------------------------------------------------------------------------------------------

## Usage

from 008_memory_monitor import MemoryMonitor\
\
\# Monitor a specific process with a 200MB threshold\
monitor = MemoryMonitor(\"chrome.exe\", threshold_mb=200.0)\
monitor.start_monitoring()
