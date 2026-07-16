# Simple Binary Extractor

This script inspects files to extract filesystem timelines, verify actual file types using hex headers, and pull out readable text strings. It helps you quickly identify basic file data and catch extension spoofing from the terminal.

## Technical Choices

* Written in Python 3 using only standard library modules, meaning it requires no external package installations.
* Uses the os module to read file statistics directly from the file system.
* Uses binary reading mode to safely open files and pull the first 4 bytes for magic number verification.
* Uses byte-based regular expressions to scan and filter out ASCII characters that are 4 or more characters long.

## Prerequisites

You only need Python 3 installed on your system. No external libraries are required.

## How to Run

Save the script as `binary_extractor.py` and run it from your terminal by passing the file path as an argument.

### Command Format

```bash
python binary_extractor.py <path_to_binary>