# System Integrity Reporter (Project 005)

A professional, modular utility designed to capture strict system metadata. This tool serves as a foundational reconnaissance script for forensic laboratories to rapidly establish the immutable environment baseline of a target machine.

## Technical Explanation

* **Direct OS Interfacing:** Utilizes the native `platform` library to interface directly with the host operating system and hardware abstraction layer, providing deterministic environment details without relying on fragile external dependencies.
* **Execution Context Awareness:** Dynamically probes the runtime state using `getattr(sys, 'frozen', False)`. This detects whether the engine is running as a raw Python script or as a compiled standalone binary (e.g., packed via PyInstaller), ensuring path resolution remains stable in production.
* **Stateless Architecture:** Implemented using class wrappers and `@staticmethod` decorators, allowing the reporting logic to be invoked instantly across massive Incident Response pipelines without the overhead of memory state instantiation.

## Problems Solved

* **Environment Baselining:** Rapidly documents and vaults the exact OS architecture, release version, and kernel build during the critical "Reconnaissance" phase of a forensic audit.
* **Binary Integrity Verification:** Helps investigators mathematically identify if the running code is operating as an authorized compiled tool or as an injected raw script in the field.
* **Automated Audit Standardization:** Standardizes how system information is structurally saved, allowing for seamless data ingestion and correlation inside centralized forensic timelines.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Structure** | `class` + `@staticmethod` | Keeps the codebase highly cohesive and reusable for larger Incident Response engines without requiring unnecessary memory state allocations. |
| **Metadata Core** | `platform` Library | It is a built-in standard. Relying purely on native modules guarantees cross-platform reliability (Windows, Linux, macOS) on isolated, air-gapped forensic hosts. |
| **Context Check** | `getattr(sys, 'frozen')` | The official Pythonic mechanism to detect if a script was bundled into an `.exe` or ELF binary, preventing catastrophic path resolution crashes in live environments. |

## Usage

This utility can be integrated into broader automation scripts or run standalone. Ensure the file is named cleanly (e.g., `system_reporter.py`) to allow seamless imports.

Run directly via the command line interface:

```bash
# Generate a baseline report in the current directory
python system_reporter.py
# System Integrity Reporter

This script collects and logs basic environment data from the host machine. It solves the need to quickly capture the operating system type, version, architecture, and runtime state into an audit file for verification or environment debugging.

## What It Solves

* Automatically identifies the core operating system name and specific build version.
* Detects the hardware architecture of the underlying machine.
* Checks if the execution context is running directly from source files or as a bundled standalone executable.
* Writes all collected data into a local log file with accurate field mappings.

## Technical Choices

* Written in Python 3 using standard library modules, so it runs out of the box without any package installations.
* Uses the platform module to read system environmental variables across different operating systems.
* Uses a sys attribute check (`sys.frozen`) to verify if the file has been bundled with compilation tools like PyInstaller.
* Uses the os module to resolve and print the absolute path of the generated output file on the host filesystem.

## Prerequisites

You only need Python 3 installed on your system. No external libraries are required.

## How to Run

Save the script as `system_reporter.py` and run it from your terminal.

### Command Format

```bash
python system_reporter.py