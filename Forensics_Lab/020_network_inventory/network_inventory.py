import sys
import time
import requests
from scapy.all import ARP, Ether, srp, sniff

class NetworkInventory:

    def __init__(self):
        self.arp_table = {}  
        print("[!] Network Inventory & ARP Monitor Active.")

    def get_vendor(self, mac_address):
        try:
            url = f"https://api.macvendors.com/{mac_address}"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            response = requests.get(url, headers=headers, timeout=3)
            if response.status_code == 200:
                return response.text.strip()
            elif response.status_code == 429:
                return "Rate Limited (API Request Limit Reached)"
            return "Unknown Manufacturer"
        except requests.RequestException:
            return "Lookup Error (API Unreachable)"

    def scan_and_identify(self, ip_range):
        if not ip_range.strip():
            print("[-] Error: Subnet range cannot be empty.")
            return

        print(f"\n[*] Scanning infrastructure on {ip_range} and resolving OUIs...")
        packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range)

        try:
            answered, _ = srp(packet, timeout=2, verbose=False)
            print("\n    IP ADDRESS      MAC ADDRESS       RESOLVED VENDOR")
            print("    " + "-" * 60)

            for _, received in answered:
                ip = received.psrc
                mac = received.hwsrc
                vendor = self.get_vendor(mac)
                print(f"    {ip:<14} {mac:<17} {vendor}")

                self.arp_table[ip] = mac
                time.sleep(1)
            print("    " + "-" * 60)
        except KeyboardInterrupt:
            print("\n[!] Inventory scan interrupted by operator. Partial baseline cached.")
        except Exception as e:
            print(f"[-] Inventory acquisition fault: {e}")

    def monitor_arp_changes(self, packet):
        if packet.haslayer(ARP) and packet[ARP].op == 2:  
            ip = packet[ARP].psrc
            mac = packet[ARP].hwsrc

            if ip in self.arp_table:
                if self.arp_table[ip] != mac:
                    print(f"\n[!!!] CRITICAL SECURITY ALERT: DETECTED ARP INCONSISTENCY [!!!]")
                    print(f"    Target IP Interface: {ip} reported a MAC address mutation!")
                    print(f"    Historical Baseline: {self.arp_table[ip]}")
                    print(f"    Anomalous New Entry: {mac} (Potential MitM Spoofing Attack!)")
            else:
                self.arp_table[ip] = mac

if __name__ == "__main__":
    inv = NetworkInventory()

    while True:
        print("\n    1. Scan & Identify Vendors (Active Discovery)")
        print("    2. Start Real-Time ARP Cache Monitor (Defensive Guard)")
        print("    0. Exit")

        try:
            choice = input("\n    Select operational path: ")

            if choice == '1':
                target = input("    Enter target network subnet (e.g., 192.168.1.0/24): ")
                inv.scan_and_identify(target)
            elif choice == '2':
                print("[*] Monitoring broadcast pool for dynamic mutations... Press Ctrl+C to terminate.")
                try:
                    sniff(filter="arp", prn=inv.monitor_arp_changes, store=0)
                except KeyboardInterrupt:
                    print("\n[*] Real-time monitoring session closed by operator.")
            elif choice == '0':
                print("[*] Deactivating database hooks.")
                sys.exit(0)
            else:
                print("[-] Invalid selection. Please try again.")
        except KeyboardInterrupt:
            print("\n[*] Deactivating database hooks.")
            sys.exit(0)
