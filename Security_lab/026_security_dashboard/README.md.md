# Security Dashboard Framework (Project 026)

A graphical user interface (GUI) framework designed to act as a central
controller for the various Python modules within the Security Lab,
providing visual feedback and parameter selection.

## Technical Explanation

-   **Event-Driven Architecture:** Utilizes the Tkinter main loop to
    manage GUI rendering and asynchronous event handling.
-   **State Management:** Maps user interactions (Checkbuttons) to
    *BooleanVar* states, allowing for dynamic configuration of backend
    tools before execution.
-   **Synchronous Progress Tracking:** Implements *ttk.Progressbar* with
    manual IDLE task updates to provide real-time visual status reports
    during intensive I/O operations (scanning/sniffing).

## Problems Solved

1.  **Operator Cognitive Load:** Simplifies complex command-line tool
    usage into a single, cohesive dashboard, reducing errors in
    configuration inputs.
2.  **Operational Visibility:** Provides visual progress markers for
    long-running scripts (like network inventory or forensic triage),
    preventing the perception of system freezes.
3.  **Unified Interface:** Acts as the integration point for all Lab
    scripts, transforming individual tools into a cohesive operational
    security system.

## Usage

from 026_security_dashboard import SecurityDashboard\
\
\# Initialize and launch the main operational GUI\
dashboard = SecurityDashboard()\
dashboard.run()
