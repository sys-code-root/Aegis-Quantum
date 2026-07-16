# Network Flow Analyzer

This script captures live network packets, tracks active TCP connections, and aggregates the total data volume passed between hosts. It solves the need to quickly identify which network flows are consuming the most bandwidth directly from your terminal.

## What It Solves

* Monitors network interfaces to filter and inspect packets containing both IP and TCP layers.
* Groups communication streams by source IP, destination IP, and destination port.
* Tracks the exact data size of each packet to accumulate total bytes per flow.
* Generates a final summary report sorted by bandwidth usage in descending order.

## Technical Choices

* Written in Python 3 for straight execution inside terminal environments.
* Uses the Scapy library to read raw network sockets and unpack layer data.
* Uses a `defaultdict(int)` from the standard collections module to efficiently track and append byte counts using a unique mapping key.
* Disables packet caching (`store=0`) inside the sniffing function to prevent high memory consumption during live streams.
* Includes dynamic argument handling to read inputs for packet counts or specific interface paths without manual script changes.

## Prerequisites

You need Python 3 and the Scapy library installed.

Install the required library using pip:

```bash
pip install scapy