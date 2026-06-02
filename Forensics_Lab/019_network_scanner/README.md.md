# ARP & ICMP Active Network Scanner (Project 019)

A network reconnaissance and forensics asset-mapping module designed to
identify live targets inside local network routing domains.

## Technical Explanation

-   **Layer 2 Broadcast Injection:** Bundles hardware Ethernet frames
    (*ff:ff:ff:ff:ff:ff*) to force every networking interface switch on
    the local wire to process the request.
-   **ARP Translation Mining:** Intercepts incoming protocol replies to
    extract raw source bindings (*received.psrc* and *received.hwsrc*),
    mapping IPs directly to physical hardware NICs.
-   **Network-Layer Inversion:** Compiles manual ICMP Echo Request
    tokens wrapped inside Time-To-Live (TTL) IP packets, assessing
    remote availability without relying on high-level OS socket
    frameworks.

## Problems Solved

1.  **Rogue Hardware Localization:** Exposes hidden or unauthorized
    computers connected to local infrastructure that bypass standard
    directory listings.
2.  **IP-to-MAC Binding Logs:** Provides authentic layer 2 hardware
    addressing records, preventing attackers from hiding behind spoofed
    dynamic IP parameters.
3.  **Defensive Firewal Triage:** Evaluates if a compromised endpoint
    drops ICMP packages while reacting to explicit network queries.

## Design Decisions: \"Why this instead of that?\"

  ------------------------ ---------------------------------- -------------------------------------------------------------------------------------------------------------------------------------
  **Discovery Protocol**   ARP Protocol Scanning              Way faster and more reliable than ICMP scanning inside local networks, as systems cannot ignore local ARP requests.
  **Packet Control**       Natively compiled Layer 2 frames   Grants full control over the header fields, bypassing the operational restrictions of standard Python socket connections.
  **Response Model**       *sr1* Framework Call               Perfect execution model for sequential target tracking; stops reading immediately after capturing the first confirmation handshake.
  ------------------------ ---------------------------------- -------------------------------------------------------------------------------------------------------------------------------------

## Usage

from 019_network_scanner import NetworkScanner\
\
\# Initialize the discovery scanner engine\
scanner = NetworkScanner()\
\
\# Example 1: Execute full local mapping sweep\
scanner.arp_scan(\"192.168.1.0/24\")\
\
\# Example 2: Probe a single host endpoint directly\
scanner.icmp_ping(\"10.0.0.15\")
