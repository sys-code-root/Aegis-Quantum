import sys
from scapy.all import sniff, IP, TCP, UDP, Ether

class PacketSniffer:
    """
    Performs network forensics by capturing and dissecting live socket packets.
    Analyzes frame metrics across Layers 2, 3, and 4 to gather digital evidence.
    """
    def __init__(self):
        self.packet_count = 0
        print("[!] Sniffer initialized. Waiting for protocol frames...")
        print("[!] Note: Admin/Sudo privileges are required to bind to the raw socket interface.")

    def packet_callback(self, packet):
        """
        Executes structural inversion and parsing on every frame pulled from the network stack.
        Acts as the primary decoder for dynamic forensic logging.
        """
        self.packet_count += 1
        print(f"\n[+] --- CAPTURED FRAME #{self.packet_count} ---")

        # Layer 2 Analysis - Hardware Addressing (Ethernet)
        if packet.haslayer(Ether):
            src_mac = packet[Ether].src
            dst_mac = packet[Ether].dst
            print(f"    [LAYER 2] MAC Interface: {src_mac} -> {dst_mac}")

        # Layer 3 Analysis - Logical Network Routing (IPv4)
        if packet.haslayer(IP):
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            proto = packet[IP].proto
            print(f"    [LAYER 3] IP Routing:    {src_ip} -> {dst_ip} (Protocol Tokens: {proto})")

        # Layer 4 Analysis - Transport Layer Sockets & Port Mapping (TCP/UDP)
        if packet.haslayer(TCP):
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
            print(f"    [LAYER 4] TCP Segment:   {src_port} -> {dst_port}")

            # Identify cleartext unencrypted web transactions (HTTP)
            if dst_port == 80 or src_port == 80:
                print("            [!!!] ALERT: Unencrypted HTTP Traffic Intercepted!")

        elif packet.haslayer(UDP):
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport
            print(f"    [LAYER 4] UDP Datagram:  {src_port} -> {dst_port}")

            # Identify name resolution operations (DNS)
            if dst_port == 53 or src_port == 53:
                print("            [!!!] ALERT: Live DNS Query Resolution Discovered!")

    def start_sniffing(self, count=10, filter_exp=""):
        """Binds to the native interface link to capture a fixed threshold of data bursts."""
        print(f"[*] Compiling network socket tap. Capturing {count} packets via filter: '{filter_exp}'")
        try:
            # store=0 prevents memory hoarding by dropping the frame array after callback execution
            sniff(filter=filter_exp, prn=self.packet_callback, count=count, store=0)
        except Exception as e:
            print(f"[-] Execution Failure: {e}")
            print("[-] Confirm if script context was initiated with administrative root privileges.")

if __name__ == "__main__":
    sniffer = PacketSniffer()

    print("\n" + "="*40)
    print("      SCAPY NETWORK ANALYZER v1.0")
    print("="*40)

    while True:
        print("\n    1. Sniff ALL traffic (10 packets)")
        print("    2. Sniff only HTTP (Port 80)")
        print("    3. Sniff only DNS (Port 53)")
        print("    0. Exit")

        choice = input("\n    Select filter configuration: ")

        if choice == '1':
            sniffer.start_sniffing(count=10)
        elif choice == '2':
            sniffer.start_sniffing(count=10, filter_exp="tcp port 80")
        elif choice == '3':
            sniffer.start_sniffing(count=10, filter_exp="udp port 53")
        elif choice == '0':
            print("[*] Terminating network socket interfaces.")
            break
