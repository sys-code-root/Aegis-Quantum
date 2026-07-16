# WSL Forensic Prober

This script inspects a Linux or WSL environment to gather basic system evidence, check file integrity, detect resource spikes, and find suspicious startup scripts. It automates manual terminal checks by logging findings directly into a file.

## What It Solves

* Checks shell startup files for unauthorized or suspicious network commands.
* Identifies running processes that exceed a set CPU usage threshold.
* Verifies real file types using hex signatures to see if an extension was modified.
* Tracks a directory for a short time to catch files being added or deleted in real time.

## Technical Choices

* Written in Python 3 for straight execution inside WSL or Linux environments.
* Uses the psutil library to safely inspect system processes and measure CPU consumption.
* Uses built-in modules like binascii and os to handle raw file bytes and read file system timestamps.
* Saves all findings automatically to a local log file named `wsl_forensic_evidence.log` with clear time markers.

## Prerequisites

You need Python 3 and the psutil library installed.

Install the required library using pip:

```bash
pip install psutil