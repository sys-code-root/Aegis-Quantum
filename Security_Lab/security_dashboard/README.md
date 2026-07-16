# Security Scan Dashboard Interface

This script builds a basic graphical user interface desktop window to configure and trigger local scanning actions. It solves the need for a simple visual control panel where users can toggle setup options before execution and track task progress visually.

## What It Solves

* Creates a desktop window interface with a fixed dimension to contain configuration controls.
* Provides selectable check buttons to toggle specific flags such as stealth mode and forensics logging.
* Includes an execution button that triggers a simulated backend scanning task.
* Loops through sequential loading increments and updates a horizontal loading bar visually in real time.
* Outputs a completion line to the standard system terminal once the simulation sequence wraps up.

## Technical Choices

* Written in Python 3 to ensure cross-compatible execution on standard desktop systems.
* Uses the native Tkinter framework to handle window setups, component frames, text labels, and button widgets.
* Uses the themed Tkinter module (ttk) to implement a clean, default configuration for the horizontal progress bar indicator.
* Employs the standard time module to run a deliberate delay cadence during the visual progress step calculation.
* Uses the update_idletasks window method to force UI rendering updates sequentially throughout the loop execution.

## Prerequisites

* Python 3 installed on your machine.
* This tool uses the standard library, so no external package installations or pip commands are required.

## How to Run

Save the script code as `security_dashboard.py` and run it from your command terminal:

```bash
python security_dashboard.py