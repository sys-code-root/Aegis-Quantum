# Master Dashboard (Project 011)

The centralized orchestration hub for your cybersecurity laboratory.
This tool integrates all forensic, defensive, and response modules into
a single, professional control panel.

## Technical Explanation

-   **Command Pattern:** Utilizes class-based methods to map user inputs
    to specific security functions, ensuring a scalable architecture.
-   **State Management:** Maintains an active loop that manages process
    execution and allows for seamless transitions between different
    security toolsets.

## Problems Solved

1.  **Operational Complexity:** Replaces multiple independent
    command-line executions with a unified, interactive interface.
2.  **Standardized Response:** Forces a consistent workflow for Incident
    Response, ensuring that every tool is utilized in the correct
    sequence.
3.  **Professional Triage:** Provides a \"ready-to-use\" environment,
    demonstrating full-stack automation skills to recruiters and peers.

## Design Decisions: \"Why this instead of that?\"

  ---------------- ------------------- -----------------------------------------------------------------------------------------------
  **Interface**    CLI Menu            Superior to GUI for Incident Response, as it is lighter, faster, and works over SSH sessions.
  **Structure**    OOP (Class)         Allows you to easily plug in your new modules as you continue developing them.
  **Navigation**   *os.system* clear   Provides a clean, \"pro-terminal\" look which is standard in low-level security tools.
  ---------------- ------------------- -----------------------------------------------------------------------------------------------

## Usage

from 011_master_dashboard import CyberSecurityDashboard\
\
\# Launch the orchestrator\
dashboard = CyberSecurityDashboard()\
dashboard.start()
