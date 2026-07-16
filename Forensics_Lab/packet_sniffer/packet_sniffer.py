import sys
from scapy.all import sniff, IP, TCP, UDP, Ether

class PacketSniffer:

    def __init__(self):
        self.packet_count = 0
        print("[!] Sniffer initialized. Waiting for protocol frames...")
        print("[!] Note: Admin/Sudo privileges are required to bind to the raw socket interface.")

    def packet_callback(self, packet):
        self.packet_count += 1
        print(f"\n[+] --- CAPTURED FRAME #{self.packet_count} ---")

        if packet.haslayer(Ether):
            print(f"    [LAYER 2] MAC Interface: {packet[Ether].src} -> {packet[Ether].dst}")

        if packet.haslayer(IP):
            print(f"    [LAYER 3] IP Routing:    {packet[IP].src} -> {packet[IP].dst} (Protocol: {packet[IP].proto})")

        if packet.haslayer(TCP):
            sport = packet[TCP].sport
            dport = packet[TCP].dport
            print(f"    [LAYER 4] TCP Segment:   {sport} -> {dport}")
            if sport == 80 or dport == 80:
                print("            [!!!] ALERT: Unencrypted HTTP Traffic Intercepted!")

        elif packet.haslayer(UDP):
            sport = packet[UDP].sport
            dport = packet[UDP].dport
            print(f"    [LAYER 4] UDP Datagram:  {sport} -> {dport}")
            if sport == 53 or dport == 53:
                print("            [!!!] ALERT: Live DNS Query Resolution Discovered!")

    def start_sniffing(self, count=10, filter_exp=""):
        print(f"[*] Compiling network socket tap. Capturing {count} packets via filter: '{filter_exp}'")
        try:
            sniff(filter=filter_exp, prn=self.packet_callback, count=count, store=0)
        except KeyboardInterrupt:
            print("\n[!] Sniffing capture paused by operator.")
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
            sys.exit(0)
        else:
            print("[-] Invalid selection. Please try again.")
