# Forensic Blackbox Analyzer (Project 017)

A continuous host-monitoring blackbox utility that records live terminal
history interactions and executes automated analysis on newly attached
physical/virtual storage media volumes.

## Technical Explanation

-   **Mountpoint Set Differentiation:** Calculates runtime differences
    between active partition structures (*psutil.disk_partitions*) using
    hash-set exclusions (*current - known*) to instantly isolate new
    hardware mount events.
-   **Stream Capture Trailing:** Monitously tracks terminal historical
    caches (*.bash_history*) to identify structural adjustments or
    environment variables passed directly into terminal interpreters.
-   **Targeted Forensic Sweeping:** Automates targeted filesystem walk
    routines (*os.walk*) on newly detected storage surfaces, hunting for
    hidden file layers (*.*) and binding their footprints to distinct
    SHA-256 signatures.

## Problems Solved

1.  **BadUSB / Rubber Ducky Interception:** Catches injection hardware
    payloads or unauthorized external disks the second they interface
    with the operating system layer.
2.  **Anti-Forensics Triage:** Logs executed bash terminal inputs
    instantly, preventing command logs from being obfuscated or erased
    by standard session termination resets.
3.  **Hidden Payload Surface Sweeping:** Automates the evaluation of
    root drives to unearth obfuscated tooling or hidden drop files
    before they can expand or run.

## Design Decisions: \"Why this instead of that?\"

  ------------------------- ---------------------- ------------------------------------------------------------------------------------------------------------------
  **Data Tracking**         Target Set Exclusion   Way more efficient than monitoring raw sector counts; tracks mount states instead of lower-level storage tables.
  **File Identification**   *errors=\'ignore\'*    Keeps parsing operational if terminal files contain unreadable symbols from network drops or breaks.
  **Interval Guard**        3-second Polling       Perfectly balances real-time interception with zero host engine performance exhaustion.
  ------------------------- ---------------------- ------------------------------------------------------------------------------------------------------------------
