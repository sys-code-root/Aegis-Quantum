# File Integrity Monitor

This script calculates file hash values and provides a method to track changes over time. It resolves the need to verify if file contents have been modified or tampered with by checking the file against a baseline hash.

## What It Solves

* Creates a sample configuration text file for immediate testing.
* Computes the initial SHA-256 baseline hash of the target file.
* Includes a built-in monitoring loop to regularly verify file signatures at specific time intervals.
* Alerts the user and stops verification if a hash mismatch is found.

## Technical Choices

* Written in Python 3 using standard library modules, requiring no external package installations.
* Uses the hashlib module to generate secure SHA-256 checksum strings.
* Reads files in 4096-byte blocks to safely handle data inside system memory.
* Uses the time module to pause execution between checks and format local timestamp logs.

## Prerequisites

You only need Python 3 installed on your system. No external libraries are required.

## How to Run

Save the script as `file_monitor.py` and run it from your terminal:

```bash
python fele_monitor.py