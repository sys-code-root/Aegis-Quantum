# System Integrity Reporter (Project 5)

A professional, modular utility to capture system metadata. This is a
foundational script for forensic labs to quickly establish the
environment baseline of a target machine.

## Technical Explanation

-   **Metadata Extraction:** Uses the *platform* library to interface
    directly with the host OS, providing reliable environment details
    without external dependencies.
-   **Context Awareness:** Detects whether the script is running as a
    Python source file or a compiled binary (*sys.frozen*), which is
    crucial when auditing environments where scripts may have been
    packed by tools like PyInstaller.

## Problems Solved

1.  **Environment Baseline:** Quickly documents the OS architecture and
    version during the \"Reconnaissance\" phase of an audit.
2.  **Binary Verification:** Helps identify if the code is running as an
    authorized compiled tool or as an raw script in the field.
3.  **Automated Auditing:** Standardizes how system information is
    saved, allowing for easier correlation in forensic timelines.

## Design Decisions: \"Why this instead of that?\"

  --------------- ---------------------------- --------------------------------------------------------------------------------------------------------------------------
  **Structure**   *class* + *staticmethod*     Keeps the code clean and reusable for larger IR (Incident Response) engines without needing state.
  **Metadata**    *platform* library           It is a built-in Python standard; it avoids dependencies and works across all platforms (Windows, Linux, macOS).
  **Context**     *getattr(sys, \'frozen\')*   This is the official way to detect if a script was bundled into an *.exe*, preventing errors in production environments.
  --------------- ---------------------------- --------------------------------------------------------------------------------------------------------------------------

## Usage

from 005_system_integrity_reporter import SystemIntegrityReporter\
\
reporter = SystemIntegrityReporter()\
reporter.generate_report(\"my_audit.log\")
