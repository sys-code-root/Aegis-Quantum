# Metadata Brief

This script reads basic file attributes directly from the file system. It solves the need to quickly check a file's exact size, octal permissions, and last modified timestamp from the terminal without opening the file itself.

## What It Solves

* Fetches file properties using standard operating system indicators.
* Displays the file size in bytes.
* Calculates file permissions and prints them in standard three-digit octal format (like 755 or 644).
* Converts the filesystem modification timestamp into a readable date and time format.

## Technical Choices

* Written in Python 3 using only standard library modules, so it requires no external package installations.
* Uses the os module to get file system diagnostics through os.stat.
* Uses bitwise operations (`& 0o777`) to isolate and format the permission bits correctly.
* Uses the datetime module to process time modifications into a clear YYYY-MM-DD HH:MM:SS format.
* Includes specific exception blocks to catch and identify missing files or permission restrictions without crashing.

## Prerequisites

You only need Python 3 installed on your system. No external libraries are required.

## How to Run

Save the script as `metadata_brief.py` and run it from your terminal by passing the file path as an argument.

### Command Format

```bash
python metadata_brief.py <path_to_artifact>