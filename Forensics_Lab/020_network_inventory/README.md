# Network Inventory & ARP Poisoning Monitor (Project 020)

An advanced network forensics module built to inventory network endpoints, map hardware vendor identities, and capture active Man-in-the-Middle (MitM) ARP spoofing attacks.

## Technical Explanation

* **OUI Resolution Pipelines:** Strips device MAC addresses to target public API databases, injecting real browser headers and intercepting API constraints (like HTTP `429 Rate Limited`) to ensure precise hardware supplier telemetry.
* **Persistent Cache Baseline:** Builds an in-memory dictionary tracking state parameters (`{IP: MAC}`). This inventory serves as an immutable source-of-truth registry that resists manipulation or self-contamination during an active threat vector.
* **Passive Traffic Dissection:** Binds asynchronous sniffing hooks to capture Opcode 2 (`ARP Reply`) frames, validation-checking incoming hardware packets against the cached network blueprint.
* **Dynamic Environment Learning:** Automatically populates and scales the internal monitoring index with new legitimate device profiles seen on the wire if the live capture mode is initiated without a pre-scanned baseline.

## Problems Solved

* **Man-in-the-Middle Interception:** Instantly exposes adversarial nodes trying to intercept or route network data by hijacking the local gateway's logical IP mapping.
* **Persistent Spoof Alerting:** Maintains defensive alerts active throughout the entire lifespan of the attack, blocking the malicious machine from silently poisoning or overwriting the tool's verified tracking table.
* **Asset Supply Chain Auditing:** Automates physical vendor enumeration across live network segments to isolate foreign, unapproved, or high-risk rogue hardware components instantly.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Verification Strategy** | Stateful Dictionary Lookup | Significantly faster and more reliable than querying remote routers repeatedly to confirm interface states. |
| **API Integration** | Headers & Rate Handling | Standard library requests trigger automated blocklists; spoofed User-Agents and explicit status code routing maintain lookup availability. |
| **Cache Resilience** | Immutable Alert Baseline | Modifying the cache post-alert auto-contaminates the engine; retaining the original true MAC guarantees persistent warning triggers. |
| **Filter Selection** | Strict BPF "arp" Filter | Offloads irrelevant protocol overhead at the kernel layer, focusing processing power entirely on target address structures. |

## Usage

This tool is optimized for interactive terminal operations. Execute the script using root or administrative permissions to allow raw network socket access:

```bash
sudo python network_inventory.py
