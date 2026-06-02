# Network Flow Analyzer (Project 007)

A network monitoring tool that aggregates traffic flow volumes, helping
to identify potential data exfiltration or C2 (Command & Control)
activity.

## Technical Explanation

-   **Packet Sniffing:** Uses the *scapy* library to hook into the
    network stack and analyze raw packets in real-time.
-   **Flow Aggregation:** Uses a *defaultdict* to track byte counts per
    unique connection tuple (Src, Dst, Port).
-   **Non-Blocking Capture:** Operates in a streamlined mode
    (*store=0*), which is memory-efficient for long-running monitoring
    tasks.

## Problems Solved

1.  **Data Exfiltration Detection:** Flags abnormal amounts of data
    moving to unknown or suspicious destinations.
2.  **C2 Identification:** Helps spot heartbeat-like communication
    patterns typical of malware.
3.  **Bandwidth Auditing:** Provides a breakdown of network usage by
    service/port.

## Design Decisions: \"Why this instead of that?\"

  ------------- --------------- -------------------------------------------------------------------------------------------
  **Library**   *scapy*         Provides granular access to protocol layers (IP/TCP) that standard socket libraries lack.
  **Storage**   *defaultdict*   Extremely fast lookup and aggregation during high-speed packet capture.
  **Memory**    *store=0*       Prevents the script from saving all packets in RAM, allowing indefinite monitoring.
  ------------- --------------- -------------------------------------------------------------------------------------------

## Usage

from 007_network_flow_analyzer import NetworkFlowAnalyzer\
\
analyzer = NetworkFlowAnalyzer()\
analyzer.start_sniffing(count=100)
