# Live Forensics Threat Hunter (Project 015)

A volatile data triage utility designed to analyze the live state of a system, catching aggressive process behavior and unauthorized foreign sockets.

## Technical Explanation

* **Live Process Triage:** Leverages a dual-pass delta calculation on `psutil.process_iter` to bypass initial zero-value measurement window bugs, capturing true execution statistics directly from volatile kernel structures.
* **Network Socket Mapping:** Maps active network socket frames (`psutil.net_connections`) to target states, parsing raw socket definitions into structured connection strings.
* **Network Boundary Validation:** Utilizes Python's native `ipaddress` module to mathematically evaluate endpoints against exact private address scopes (RFC 1918) and loopback ranges, completely eliminating the false negatives caused by naive string-prefix matching.

## Problems Solved

* **Cryptojacking Mitigation:** Immediately alerts on anomalous CPU constraints caused by unauthorized cryptocurrency miners or hidden loops masquerading as background system tasks.
* **Volatile Evidence Capture:** Collects memory-reliant data points—such as ephemeral connections—that are permanently wiped if the system undergoes a hard reboot or clear cycle.
* **Command & Control Discovery:** Exposes the exact external IP addresses and target ports communicating actively with the compromised host machine.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Data Scope** | Live Execution Pool | Safer than standard memory dumps when disk space, parsing overhead, or operational uptime limits raw preservation tactics. |
| **Network Level** | Connection State Filtering | Focuses specifically on `ESTABLISHED` channels to filter out irrelevant listening sockets and dead telemetry noise. |
| **IP Validation** | Native `ipaddress` Engine | String filtering fails on edge cases (like dynamic public ranges); boolean class checks (`is_private`) ensure zero-error subnet mapping. |
| **Privilege Guard** | Explicit Exception Blocks | Prevents host access restrictions or missing root privileges from breaking standard process list scanning routines. |

## Usage

This tool can be executed directly from the terminal to initiate an immediate system-wide live triage:

```bash
python threat_hunter.py
