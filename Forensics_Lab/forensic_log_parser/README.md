# Forensic Log Parser

This script scans log files line by line to detect specific security keywords and error codes. It solves the need to manually read through massive text logs to find authentication failures, permission errors, or critical alerts by automatically isolating suspicious events.

## What It Solves

* Automatically searches for security-relevant terms including FAILED, ERROR, DENIED, CRITICAL, AUTH_FAILURE, INVALID, ROOT, and SUDO.
* Performs case-insensitive matching so no variations are missed.
* Tracks exact line numbers for every match to make manual verification faster.
* Writes a clean text report summarizing the findings or confirming if the log is clear.

## Technical Choices

* Written in Python 3 using only standard library modules, requiring no external package installations.
* Uses the built-in re module to compile a regular expression pattern for fast word matching.
* Streams the target file line by line to keep memory consumption low, even when reading massive system log files.
* Uses the errors="ignore" parameter when opening files to prevent execution crashes if the log contains corrupted or non-UTF-8 characters.
* Implements the datetime module to add a precise generation timestamp to the final report.

## Prerequisites

You only need Python 3 installed on your system. No external libraries are required.

## How to Run

Save the script as `log_parser.py` and run it from your terminal by passing the target log file path as an argument.

### Command Format

```bash
python log_parser.py <path_to_log>