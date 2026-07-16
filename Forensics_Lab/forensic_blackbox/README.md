# Forensic Blackbox

This script monitors terminal command history and new storage mounts in real time. It solves the need to log executed commands from Bash history files and automatically inspects newly connected storage drives for hidden files.

## What It Solves

* Tracks the `~/.bash_history` file and logs new commands as soon as the file modification time changes.
* Detects when a new storage drive or partition is mounted to the system.
* Scans newly mounted storage volumes automatically to find hidden files (files that start with a dot).
* Calculates the SHA-256 hash of any discovered hidden files to log their integrity.

## Technical Choices

* Written in Python 3 for direct terminal execution.
* Uses the psutil library to check disk partitions and catch hardware changes.
* Uses the hashlib module to generate SHA-256 checksums, reading files in 4096-byte blocks to safely handle system memory.
* Uses the os module to track file modification timestamps and recursively look through directories using os.walk.
* Saves all captured data with timestamp markers into a local log file named `blackbox_evidence.log`.

## Prerequisites

You need Python 3 and the psutil library installed.

Install the required library using pip:

```bash
pip install psutil