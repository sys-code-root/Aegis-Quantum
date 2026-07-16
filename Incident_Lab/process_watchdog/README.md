# Process Watchdog

This script monitors running system processes against an allowed whitelist and automatically terminates any unauthorized applications. It solves the need to enforce a strict software execution policy on a machine, preventing unapproved programs from staying active.

## What It Solves

* Constantly scans active system processes using a case-insensitive check.
* Automatically protects critical operating system tasks (like system, registry, smss.exe, csrss.exe) and core Python binaries to prevent system crashes.
* Shuts down unauthorized processes immediately using system termination signals.
* Runs on a continuous loop to catch and kill unapproved software as soon as it opens.

## Technical Choices

* Written in Python 3 for straightforward terminal deployment.
* Uses the psutil library to loop through active system PIDs, pull image names, and terminate processes.
* Uses a lowercase set layout to handle the whitelist efficiently with case-insensitive tracking.
* Uses standard command-line arguments to build the whitelist dynamically at runtime, falling back to a preconfigured list of default tools (like bash, powershell, or chrome) if no parameters are passed.
* Includes targeted exception blocks for NoSuchProcess, AccessDenied, and ZombieProcess to safely bypass protected system components without crashing the script.

## Prerequisites

You need Python 3 and the psutil library installed.

Install the required library using pip:

```bash
pip install psutil