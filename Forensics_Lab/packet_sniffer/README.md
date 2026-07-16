# Scapy Network Analyzer

This script captures and inspects live network traffic across multiple protocol layers. It solves the need to quickly analyze network packets from the terminal, showing Layer 2 MAC addresses, Layer 3 IP addresses, and Layer 4 TCP/UDP ports while highlighting unencrypted web traffic and DNS queries.

## What It Solves

* Captures live network packets passing through your network interface card.
* Decodes ethernet frames to display source and destination MAC addresses.
* Extracts IPv4 data to show routing paths and underlying protocol numbers.
* Inspects TCP segments and UDP datagram ports to check active connections.
* Automatically triggers console alerts when unencrypted HTTP traffic (port 80) or active DNS queries (port 53) pass through.

## Technical Choices

* Written in Python 3 for quick deployment and execution.
* Uses the Scapy library to handle raw socket manipulation and packet dissecting safely.
* Sets the packet storage option to zero (`store=0`) inside the sniffing function to prevent high memory consumption during live captures.
* Implements a simple command-line text menu using a standard loop so you can select specific traffic filters without changing the code.

## Prerequisites

You need Python 3 and the Scapy library installed on your system.

Install Scapy using pip:

```bash
pip install scapy