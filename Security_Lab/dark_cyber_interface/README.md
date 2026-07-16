# Dark Theme Auditor Interface

This script builds a basic graphical user interface window that functions as a dark-themed status dashboard shell. It solves the need for a clean, distraction-free desktop window with a custom menu navigation system to control scanning workflows and display setup info.

## What It Solves

* Spawns a desktop workspace window using custom dimensions and a fixed dark layout.
* Configures an upper menu bar grouped into operations and details sections.
* Simulates backend state preparation by routing menu clicks to standard terminal log outputs.
* Triggers an explicit informational dialog box pop-up over the interface to show application specifications.
* Renders a central status monitor text using high-contrast monospace characters.

## Technical Choices

* Written in Python 3 for immediate portability across different operating systems.
* Uses the native Tkinter framework to structure windows, manage menu objects, and handle widget grids.
* Uses the standard Tkinter messagebox submodule to prompt asynchronous windows on top of the main thread.
* Embeds explicit hex color parameters to style layout items uniformly without loading separate theme files.

## Prerequisites

* Python 3 installed on your local computer.
* This interface relies completely on standard Python libraries, so there is no need for external pip installations.

## How to Run

Save the script code as `auditor_ui.py` and run it from your command terminal:

```bash
python auditor_ui.py