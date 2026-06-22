# ARP & ICMP Active Network Scanner (Project 019)

A network reconnaissance and forensics asset-mapping module designed to identify live targets inside local network routing domains.

## Technical Explanation

* **Layer 2 Broadcast Injection:** Bundles hardware Ethernet frames (`ff:ff:ff:ff:ff:ff`) to force every networking interface switch on the local wire to process the tracking packet.
* **ARP Translation Mining:** Intercepts incoming protocol replies to extract raw source bindings (`received.psrc` and `received.hwsrc`), mapping IP addresses directly to physical hardware NICs.
* **Network-Layer Inversion:** Compiles manual ICMP Echo Request tokens wrapped inside Time-To-Live (TTL) IP packets, assessing remote availability without relying on high-level OS socket frameworks.
* **Multi-Level Signal Trapping:** Implements localized and global error interceptors for software interruption signals (`KeyboardInterrupt`), ensuring the operator can instantly terminate a broad subnet sweep without crashing the system stack.
* **Input Validation Sanitization:** Features runtime verification via string manipulation (`.strip()`) to capture empty or malformed targets before they reach the raw network socket interface, preventing low-level library faults.

## Problems Solved

* **Rogue Hardware Localization:** Exposes hidden, forgotten, or unauthorized computers connected to local infrastructure that intentionally bypass standard directory listings or active domain controllers.
* **IP-to-MAC Binding Logs:** Provides authentic Layer 2 hardware addressing records, preventing malicious agents from hiding their infrastructure footprints behind spoofed or dynamic IP parameters.
* **Defensive Firewall Triage:** Evaluates host responsiveness and policies to detect if a compromised or target endpoint drops ICMP packages while reacting to explicit network layer queries.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Discovery Protocol** | ARP Protocol Scanning | Way faster and more reliable than ICMP scanning inside local networks, as systems cannot ignore or drop local ARP broadcast requests. |
| **Packet Control** | Natively Compiled Frames | Grants full control over the header fields via Scapy layering, bypassing the strict operational restrictions of standard Python socket connections. |
| **Response Model** | `sr1` Framework Call | Perfect execution model for sequential target probing; stops reading immediately after capturing the first confirmation handshake from the host. |
| **Signal Resilience** | Multi-Tiered Exception Traps | Standard terminal loops crash abruptly on user breaks; custom signal isolation keeps the program clean and operational during active recon workflows. |

## Usage

This tool features an interactive reconnaissance menu. Run the application with root or administrative privileges to enable raw socket operations:

```bash
sudo python network_scanner.py
