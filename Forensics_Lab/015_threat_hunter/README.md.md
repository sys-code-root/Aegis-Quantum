# Live Forensics Threat Hunter (Project 015)

A volatile data triage utility designed to analyze the live state of a
system, catching aggressive process behavior and unauthorized foreign
sockets.

## Technical Explanation

-   **Live Process Triage:** Uses *psutil.process_iter* to capture
    execution statistics directly from volatile kernel structures
    without pausing system activity.
-   **Network Socket Inversion:** Maps network socket frames
    (*psutil.net_connections*) to target states, parsing raw socket
    definitions into structured strings.
-   **Boundary Filtering:** Evaluates endpoints against standard private
    address scopes (RFC 1918) to isolate rogue external communication
    attempts (Reverse Shells / C2 channels).

## Problems Solved

1.  **Cryptojacking Mitigation:** Immediately alerts on anomalous CPU
    constraints caused by unauthorized cryptocurrency miners
    masquerading as background system tasks.
2.  **Volatile Evidence Capture:** Collects memory-reliant data
    points---such as ephemeral connections---that are permanently wiped
    if the system undergoes a hard reboot.
3.  **Command & Control Discovery:** Exposes the exact IP addresses and
    target ports communicating actively with the compromised host
    machine.

## Design Decisions: \"Why this instead of that?\"

  --------------------- -------------------------------- ---------------------------------------------------------------------------------------------------------------
  **Data Scope**        Live Execution Pool              Safer than standard memory dumps when disk space or operational uptime limits raw preservation tactics.
  **Network Level**     Connection State Filtering       Focuses specifically on *ESTABLISHED* channels to filter out irrelevant listening sockets and dead telemetry.
  **Privilege Guard**   Explicit *AccessDenied* blocks   Prevents kernel stack access restriction drops from breaking standard process list scanning.
  --------------------- -------------------------------- ---------------------------------------------------------------------------------------------------------------

## Usage

from 015_threat_hunter import ThreatHunter\
\
\# Instantiate hunter with a custom 15% alert threshold\
hunter = ThreatHunter(cpu_threshold=15.0)\
hunter.scan_processes()\
hunter.scan_network_connections()
