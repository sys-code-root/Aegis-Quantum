# Suspicious Import Scanner

This script analyzes Python source files to find imported libraries that could be used for risky operations like executing shell commands, capturing keystrokes, or exfiltrating data. It solves the need to quickly flag potentially unsafe dependencies inside a script before running it.

## What It Solves

* Parses code safely to find risk-heavy modules like subprocess, socket, pynput, and cryptography.
* Detects standard imports like `import os`.
* Detects from-style imports like `from requests import get`.
* Identifies dynamic import calls such as `__import__('base64')`.
* Isolates the base package names to match against a hardcoded watchlist dictionary.

## Technical Choices

* Written in Python 3 using only standard library modules, so it runs without extra package installations.
* Uses the built-in ast module to parse the target script into an Abstract Syntax Tree. This evaluates actual code structure instead of using unreliable regular expression text matching.
* Uses ast.walk to recursively check every functional node inside the code tree.
* Utilizes a set to store found libraries, avoiding duplicate alerts for the same module.

## Prerequisites

You only need Python 3 installed on your system. No external libraries are required.

## How to Run

Save the script as `import_scanner.py` and run it from your terminal.

### Command Format

```bash
python import_scanner.py