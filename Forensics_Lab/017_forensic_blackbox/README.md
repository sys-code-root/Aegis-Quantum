# Forensic Blackbox Analyzer (Project 017)

A continuous host-monitoring blackbox utility that records live terminal history interactions and executes automated analysis on newly attached physical or virtual storage media volumes.

## Technical Explanation

* **Mountpoint Set Differentiation:** Calculates runtime differences between active partition structures using `psutil.disk_partitions(all=True)` via hash-set exclusions (`current - known`). This instantly isolates new virtualized, WSL (drvfs), or hardware mount events.
* **I/O Optimized History Trailing:** Tracks terminal historical caches (`.bash_history`) by validating the file's modification timestamp (`os.path.getmtime`) first. The script only executes a read operational parse if new data has actually been flushed to disk, eliminating CPU/disk bottlenecks.
* **Targeted Forensic Sweeping:** Automates structural filesystem walk routines (`os.walk`) on newly detected storage boundaries, hunting specifically for hidden file layers (`.`) and binding their footprints to cryptographic SHA-256 signatures.

## Problems Solved

* **BadUSB / Rubber Ducky Interception:** Catches weaponized injection hardware payloads or unauthorized external disks the exact second they interface with the operating system layer.
* **Anti-Forensics Triage:** Logs executed bash terminal inputs instantly during the active session, preventing dynamic command trails from being obfuscated or erased by standard session termination resets.
* **Hidden Payload Surface Sweeping:** Automates the evaluation of newly mounted surfaces to unearth obfuscated tooling or hidden drop files before they can execute or expand within the host environment.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Data Tracking** | Target Set Exclusion | Way more efficient than monitoring raw sector counts; tracks state architecture deltas instead of lower-level storage allocation tables. |
| **History Optimization** | `mtime` Verification | Avoids continuous disk read loops on every cycle. Parsing only triggers when the kernel flushes changes to the history file. |
| **Scope Strategy** | `all=True` Partitioning | Standard partition arrays miss peripheral system attachments in containerized or WSL environments; structural flags catch all dynamic boundaries. |

## Usage

This tool is optimized for continuous background operations via the command line interface (CLI):

```bash
python forensic_blackbox.py
