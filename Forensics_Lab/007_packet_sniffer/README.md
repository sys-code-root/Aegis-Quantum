# Scapy Network Packet Sniffer (Project 018)

A low-level network forensics utility capable of parsing raw packet frames from network interface cards and mapping header signatures across Layers 2, 3, and 4.

## Technical Explanation

* **Layer Demultiplexing:** Evaluates protocol fields within Scapy's structural mapping classes (`packet.haslayer`) to dynamically isolate and split nested encapsulation frames.
* **Socket Dissection:** Strips raw hexadecimal packet data into structured console streams, mapping explicit network hardware and logical layers (MAC targets, IPs, and Transport Ports).
* **Zero-Overhead Buffer Management:** Drops network packets from system memory arrays immediately after callback execution via `store=0` parameters, enabling indefinite forensic captures without memory hoarding.
* **Signal Control Integration:** Intercepts runtime keyboard exceptions inside the sniffing engine, allowing operators to pause ongoing packet captures cleanly without dropping out of the application menu context.

## Problems Solved

* **Cleartext Credential Leakage:** Flags insecure transmission vectors by isolating unencrypted Port 80 HTTP payloads where authentication tokens, parameters, or session cookies might be exposed.
* **Data Exfiltration Trailing:** Trailing unexpected outbound communication flows across Layers 3 and 4 helps teams detect hidden exfiltration patterns or covert reverse connection tunnels.
* **Malicious DNS Analysis:** Intercepts Port 53 UDP traffic pipelines to expose dynamic lookups, uncovering active Command and Control (C2) beaconing mechanisms using domain generation algorithms (DGAs).

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Parsing Engine** | Scapy Library | Native packet compilation provides reliable layer mapping and field decoding without the need to manually parse slicing offsets on raw binary buffers. |
| **Memory Strategy** | `store=0` Configuration | Discards packet objects instantly post-callback processing, preventing kernel buffer exhaustion or process crashes during intense traffic bursts. |
| **Interception Mode** | BPF Socket Filters | Offloads early protocol matching criteria (`tcp port 80`, `udp port 53`) straight to kernel-level subroutines, conserving user-space execution power. |
| **UI Control** | In-Engine Trap | Handling runtime exceptions inside the capture module isolates the asynchronous network thread, safeguarding menu persistence and interface states. |

## Usage

This tool is built with an interactive console menu optimized for live-response operations. Run it directly with administrative root privileges:

```bash
sudo python packet_sniffer.py
