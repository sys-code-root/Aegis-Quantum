# Sentinel Watchdog

This script monitors a specific directory in real time to detect any file modifications, additions, deletions, or new hidden files. It solves the need to track directory changes and maintain an audit log of file modifications using file integrity hashing.

## What It Solves

* Automatically scans a directory and all its subdirectories for changes.
* Detects when files are modified by comparing their SHA-256 hashes.
* Highlights when new hidden files (files starting with a dot) are introduced.
* Tracks deleted files and logs the exact timestamp of each activity.

## Technical Choices

* Written in Python 3 using only standard library modules, meaning it requires no extra package installations.
* Uses the hashlib module to generate SHA-256 checksums, reading files in 4096-byte blocks to manage system memory efficiently when processing larger files.
* Uses os.walk to recursively traverse the entire target folder structure.
* Implements an infinite time loop with a default 2-second sleep interval to check for changes without overworking the CPU.
* Includes exception blocks to catch permission or missing file errors if a file is modified or deleted mid-scan.

## Prerequisites

You only need Python 3 installed on your system. No external libraries are required.

## How to Run

Save the script as `sentinel_watchdog.py` and run it from your terminal by passing the target directory path as an argument.

### Command Format

```bash
python sentinel_watchdog.py <directory_path>