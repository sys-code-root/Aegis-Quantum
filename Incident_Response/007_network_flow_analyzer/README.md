# Network Flow Analyzer (Project 007)

A network monitoring tool that aggregates traffic flow volumes, helping to identify potential data exfiltration, stealth reconnaissance scans, or C2 (Command & Control) activity.

## Technical Explanation

* **Full-Frame Packet Sniffing:** Hooks into the network stack using the `scapy` library to analyze raw packets in real-time. Volume aggregation uses full-frame diagnostics (`len(packet)`) to guarantee the inclusion of TCP control overhead and payloadless signaling.
* **Flow Aggregation Metrics:** Tracks byte counts inside an optimized in-memory `defaultdict` using a unique connection tuple key (`Src_IP`, `Dst_IP`, `Dst_Port`) to build a stateful NetFlow architecture.
* **Non-Blocking Buffer Capture:** Operates without memory-hoarding structures (`store=0`), dropping analyzed packet objects instantly post-callback execution to allow long forensic auditing sessions without freezing host resources.
* **Flexible CLI Parametrization:** Integrates a dynamic argument evaluation block (`sys.argv`) that automatically detects parameter positions, mapping packet thresholds and specific interface wrappers seamlessly.

## Problems Solved

* **Data Exfiltration Detection:** Flags abnormal spikes in communication volume migrating toward unknown external infrastructure or unverified target endpoints.
* **Stealth Reconnaissance Isolation:** Captures payloadless control packages (such as `SYN`, `ACK`, or `FIN` flags used in port mapping/scans) that standard payload-only parsers fail to track.
* **Bandwidth Overhead Auditing:** Provides a structural data summary broken down by network sockets, allowing rapid diagnostic profiling of network service consumption.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Volume Metric** | Full Frame `len(packet)` | Using payload length (`len(packet[TCP].payload)`) leaves a blind spot for scans and handshake signatures. Full frame audits capture 100% of network data metrics. |
| **Storage Model** | `defaultdict(int)` | Drastically outperforms regular dictionary error-checking loops (`try/except`), maximizing throughput during rapid, high-volume socket streaming. |
| **Memory Isolation** | `store=0` Optimization | Prevents the Python runtime from logging massive raw packet matrices inside the host's heap space, keeping RAM completely flat. |
| **CLI Wrapper** | Bidirectional Argument Parser | Accepts parameters in any arbitrary order (e.g., `count` before or after `interface`), improving operational speed for security operators under triage pressure. |

## Usage

This tool features a smart command-line interface. Run the script directly by passing your capture targets (supports passing only count, only interface, or both in any order):

```bash
# Example 1: Sniff 100 packets on the default interface
python flow_analyzer.py 100

# Example 2: Sniff 500 packets explicitly targetting interface eth0
python flow_analyzer.py eth0 500

# Example 3: View the built-in inline usage guidelines
python flow_analyzer.py --help
