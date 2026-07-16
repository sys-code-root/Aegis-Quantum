# Network Inventory and ARP Monitor

This script maps active devices on a local network and monitors traffic for unauthorized configuration changes. It solves the need to discover connected equipment, check device manufacturers using their hardware addresses, and track down potential Man-in-the-Middle or ARP spoofing attacks from the terminal.

## What It Solves

* Active Discovery: Sends broadcast frames across a local subnet to build an inventory of live IP and MAC addresses.
* Vendor Lookup: Connects to a public API to resolve MAC addresses to their specific hardware manufacturers.
* Integrity Monitoring: Sniffs ongoing network packets to spot instances where an already cached IP address suddenly starts reporting a different MAC address.

## Technical Choices

* Written in Python 3 for simple terminal execution and deployment.
* Uses the Scapy library to assemble raw Layer 2 network frames and run a live packet sniffing loop.
* Uses the Requests library to send HTTP GET requests to the MacVendors API.
* Implements an inside-memory dictionary baseline to track active pairs and notice variations instantly.
* Sets packet storage to zero (`store=0`) during active sniffing to save system memory over long runtimes.
* Includes a 1-second delay between API lookups to respect external server rate limits.

## Prerequisites

You need Python 3 and the scapy and requests libraries installed.

Install the required libraries using pip:

```bash
pip install scapy requests