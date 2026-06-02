# Scapy Network Packet Sniffer (Project 018)

A low-level network forensics utility capable of parsing raw packet
frames from network interface cards and mapping header signatures across
Layers 2, 3, and 4.

## Technical Explanation

-   **Layer Demultiplexing:** Evaluates protocol fields within Scapy\'s
    structural mapping classes (*packet.haslayer*) to dynamically split
    nested packets.
-   **Socket Dissection:** Strips raw hexadecimal bytes into structured
    text fields, mapping explicit network definitions (MAC IDs, IPs,
    Ports).
-   **Buffer Management:** Drops network packets from system memory
    arrays immediately after evaluation via *store=0* parameters,
    allowing long forensic sessions to execute without freezing host
    environments.

## Problems Solved

1.  **Cleartext Credential Leakage:** Flags insecure configurations by
    isolating raw Port 80 payloads where application passwords or
    session cookies might be leaked.
2.  **Data Exfiltration Trailing:** Tracks unexpected outbound
    connections, helping identify hidden data exfiltration attempts over
    non-standard interfaces.
3.  **Malicious DNS Analysis:** Intercepts port 53 traffic pipelines to
    uncover Command and Control beacon mechanisms using domain
    generation algorithms (DGAs).

## Design Decisions: \"Why this instead of that?\"

  ------------------- ------------------------- -------------------------------------------------------------------------------------------------------------------------
  Parsing Engine      Scapy Library             Native packet compilation provides reliable extraction of complex fields without manually slicing raw hex offset bytes.
  Memory Strategy     *store=0* Configuration   Prevents kernel buffer panics or script termination during sudden network traffic spikes.
  Interception Mode   BPF Socket Filters        Offloads early protocol filtering (*tcp port 80*) to kernel-level subroutines, saving application processor overhead.
  ------------------- ------------------------- -------------------------------------------------------------------------------------------------------------------------

## Usage

To integrate the *PacketSniffer* into your forensic automation pipeline
or run it programmatically, instantiate the class and define the burst
threshold:

from 018_packet_sniffer import PacketSniffer\
\
\# Initialize the forensic network decoder\
sniffer = PacketSniffer()\
\
\# Example 1: Capture 5 packets of any protocol type\
sniffer.start_sniffing(count=5)\
\
\# Example 2: Target cleartext web traffic specifically (Requires
root/sudo privileges)\
sniffer.start_sniffing(count=20, filter_exp=\"tcp port 80\")\
\
\# Example 3: Monitor malicious DNS resolution attempts\
sniffer.start_sniffing(count=10, filter_exp=\"udp port 53\")
