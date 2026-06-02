# Network Inventory & ARP Poisoning Monitor (Project 020)

An advanced network forensics module built to inventory network
endpoints, map hardware vendor identities, and capture active
Man-in-the-Middle (MitM) ARP spoofing attacks.

## Technical Explanation

-   **OUI Resolution Pipelines:** Strips device MAC addresses to target
    public API databases, mapping vendor metrics to verify supply chain
    asset classes.
-   **Stateful Cache Auditing:** Builds an in-memory dictionary tracking
    state parameters (*{IP: MAC}*). This baseline serves as a
    source-of-truth registry to calculate unexpected changes.
-   **Passive Traffic Dissection:** Binds sniffer hooks to capture
    opcode 2 (*ARP Reply*) frames, validating incoming data packages
    against the established baseline profile.

## Problems Solved

1.  **Man-in-the-Middle Interception:** Instantly exposes network
    attackers attempting to divert traffic by mapping their malicious
    network cards to legitimate gateway IP addresses.
2.  **Hardware Spoof Detection:** Identifies network anomalies where
    corporate assets suddenly report changing hardware characteristics.
3.  **Asset Supply Chain Auditing:** Automates physical vendor
    enumeration across subnets to isolate foreign, unapproved hardware
    equipment instantly.

## Design Decisions: \"Why this instead of that?\"

  --------------------------- ----------------------------- --------------------------------------------------------------------------------------------------------------------------
  **Verification Strategy**   Stateful Dictionary Lookup    Significantly faster and more reliable than querying remote routers repeatedly to confirm interface states.
  **API Integration**         Integrated *time.sleep*       Protects the analysis environment from getting rate-limited or banned by public lookup servers during broad scans.
  **Filter Selection**        Strict BPF *\"arp\"* Filter   Offloads irrelevant protocol overhead at the kernel layer, focusing processing power entirely on target address strings.
  --------------------------- ----------------------------- --------------------------------------------------------------------------------------------------------------------------

## Usage

from 020_network_inventory import NetworkInventory\
\
\# Initialize the stateful network monitor\
inv = NetworkInventory()\
\
\# Step 1: Baseline local assets (Fills the verification lookup map)\
inv.scan_and_identify(\"192.168.1.0/24\")\
\
\# Step 2: Launch passive background interception (Requires
administrative root access)\
from scapy.all import sniff\
sniff(filter=\"arp\", prn=inv.monitor_arp_changes, store=0)
