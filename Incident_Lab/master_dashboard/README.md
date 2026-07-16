# Cybersecurity Master Dashboard

This script provides a central command-line menu interface to manage and launch individual security tools from a single console. It solves the need to remember filenames and command configurations by organizing separate script files under one unified text menu.

## What It Solves

* Centralizes security operations by linking four dedicated scripts into one runner.
* Provides quick menu options to switch between network reconnaissance, system defense, incident response, and cloud alerts.
* Prompts users for additional parameters when needed, such as catching a target directory path before launching the incident response cleanup engine.
* Prevents total execution crashes if a sub-module script is missing or encounters a runtime error.

## Technical Choices

* Written in Python 3 using only standard library modules, requiring no extra package installations for the hub itself.
* Uses the subprocess module along with `sys.executable` to invoke scripts safely using the same Python runner path currently active.
* Uses the os module to identify if the current environment is running on Windows (`nt`) or Linux/Unix to run the correct terminal clear screen command (`cls` vs `clear`).
* Implements a persistent while loop with user-input routing to keep the control menu running until option 0 is picked or a KeyboardInterrupt occurs.

## Prerequisites

* Python 3 installed on your system.
* The required sub-modules (`flow_analyzer.py`, `watchdog.py`, `ir_engine.py`, and `cloud_alert.py`) must be placed in the exact same directory as this dashboard file.
* Note that some of the sub-modules launched by this script may require administrative or root privileges to bind to network interfaces or terminate unauthorized system processes.

## How to Run

Save the script as `dashboard.py` and execute it from your terminal:

```bash
python dashboard.py