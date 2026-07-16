# Hidden File Detector

This script scans a directory recursively to find and count hidden files and folders. It solves the need to quickly identify hidden configuration items or dotfiles buried inside deep directory structures directly from the command line.

## What It Solves

* Automatically walks through a target folder and all of its subfolders.
* Identifies any directory starting with a dot.
* Identifies any file starting with a dot.
* Counts the total number of hidden items and prints their full system paths.

## Technical Choices

* Written in Python 3 using only standard library modules, meaning it requires no extra package installations.
* Uses the os module to run an os.walk loop, which handles directory traversal efficiently without loading everything into memory at once.
* Uses simple string evaluation with startswith('.') to filter hidden filesystem objects.
* Uses the sys module to capture command-line arguments, with a built-in fallback to the current directory if no path is provided.

## Prerequisites

You only need Python 3 installed on your system. No external libraries are required.

## How to Run

Save the script as `hidden_detector.py` and run it from your terminal.

### Command Format

```bash
python hidden_detector.py <directory_path>