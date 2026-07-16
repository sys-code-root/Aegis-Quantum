# Scapy Network Scanner

This script discovery tool scans local networks to find active devices and test specific hosts. It solves the need for a quick terminal tool to map a subnet using ARP requests or check single host availability using custom ICMP pings without needing large third-party scanning tools.

## What It Solves

* Discovers active machines on a local subnet using Layer 2 ARP broadcast frames.
* Targets individual IP endpoints using custom Layer 3 ICMP echo requests to see if they are active.
* Identifies both the IP addresses and the physical MAC addresses of online devices on your network.

## Technical Choices

* Written in Python 3 for straight execution inside terminal environments.
* Uses the Scapy library to manually craft network packets at different layers of the network stack.
* Uses Scapy's srp function to send and receive custom Ethernet/ARP frames at Layer 2.
* Uses Scapy's sr1 function to send a single custom IP/ICMP packet and wait for one response at Layer 3.
* Implements a standard while loop to present a text-based menu for selecting scanning modes directly from the terminal prompt.

## Prerequisites

You need Python 3 and the Scapy library installed on your system.

Install Scapy using pip:

```bash
pip install scapy