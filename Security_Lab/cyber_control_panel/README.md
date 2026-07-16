# Cyber Security Control Panel Interface

This script builds a basic graphical user interface desktop window that serves as a visual dashboard status layout. It solves the need for a simple visual indicator window that shows a running configuration state and provides a direct terminal shutdown control.

## What It Solves

* Spawns a desktop workspace window with specific dimensions to house status readouts.
* Applies a clean dark background color to make monitoring text easier to view.
* Displays a clear status message in a distinct monospace format to verify that operational checks are active.
* Integrates a responsive button widget that hooks into the main window quit mechanism to close the loop cleanly.
* Outputs a startup message directly to the background terminal pipeline to verify thread initialization.

## Technical Choices

* Written in Python 3 for immediate portability across different operating systems.
* Uses the built-in Tkinter framework to draw native window elements, labels, and button widgets.
* Leverages basic color styling definitions via standard hexadecimal hex strings and layout padding variables.
* Uses the native window mainloop engine to handle standard frame updates and click signals natively.

## Prerequisites

* Python 3 installed on your computer.
* This interface relies entirely on standard built-in modules, so no third-party package installations or pip operations are necessary.

## How to Run

Save the provided code block as `control_panel.py` and run the script from your terminal:

```bash
python control_panel.py