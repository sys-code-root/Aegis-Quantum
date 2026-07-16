# Process Memory Monitor

This script tracks the memory usage of a specific process by name in real time. It solves the need to monitor running applications for memory leaks or high resource consumption, printing immediate status alerts if consumption goes over a set limit.

## What It Solves

* Searches the active system process list using a case-insensitive name match.
* Measures the Resident Set Size (RSS) memory footprint of the targeted application.
* Displays a high-usage alert if the memory usage exceeds a specified threshold in Megabytes.
* Automatically handles process termination, moving back into a scanning mode to re-detect the application if it restarts.

## Technical Choices

* Written in Python 3 for portability and direct execution from the command line.
* Uses the psutil library to safely inspect system process identifiers and retrieve real-time memory metrics.
* Caches the target process instance internally to avoid scanning the entire process table on every single loop iteration.
* Handles AccessDenied and NoSuchProcess exceptions to prevent crashes when encountering protected system processes or tasks that exit during a check.

## Prerequisites

You need Python 3 and the psutil library installed.

Install the required library using pip:

```bash
pip install psutil