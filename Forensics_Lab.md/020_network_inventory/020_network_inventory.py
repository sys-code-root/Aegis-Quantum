import sys
import time
import requests
from scapy.all import ARP, Ether, srp, sniff

class NetworkInventory:
    """
    Manages local network asset attribution and security baseline monitoring.
    Performs hardware vendor identification and real-time ARP Spoofing detection.
    """
    def __init__(self):
        self.arp_table = {}  # Internal state cache mapping {IP: MAC}
        print("[!] Network Inventory & ARP Monitor Active.")

    def get_vendor(self, mac_address):
        """
        Queries an external OUI database API to identify device manufacturers.
        Uses the first 3 bytes (Organizationally Unique Identifier) of the MAC.
        """
        try:
            url = f"https://api.macvendors.com/{mac_address}"
            # Low timeout prevents API bottlenecks from freezing the packet processing loop
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                return response.text
            return "Unknown Manufacturer"
        except requests.RequestException:
            return "Lookup Error (API Unreachable/Offline)"

    def scan_and_identify(self, ip_range):
        """Scans the designated network segment and builds the initial cache baseline."""
        print(f"\n[*] Scanning infrastructure on {ip_range} and resolving OUIs...")
        packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range)

        try:
            answered, _ = srp(packet, timeout=2, verbose=False)
            print("\n    IP ADDRESS     MAC ADDRESS       RESOLVED VENDOR")
            print("    " + "-" * 60)

            for _, received in answered:
                ip = received.psrc
                mac = received.hwsrc
                vendor = self.get_vendor(mac)
                print(f"    {ip:<14} {mac:<17} {vendor}")

                # Commit tracking state to live verification cache
                self.arp_table[ip] = mac
                # Small sleep window to respect free public API rate limits
                time.sleep(1)
            print("    " + "-" * 60)
        except Exception as e:
            print(f"[-] Inventory acquisition fault: {e}")

    def monitor_arp_changes(self, packet):
        """Intercepts incoming ARP replies to detect poisoning attempts (Man-in-the-Middle)."""
        if packet.haslayer(ARP) and packet[ARP].op == 2:  # Target packet is an ARP Reply
            ip = packet[ARP].psrc
            mac = packet[ARP].hwsrc

            if ip in self.arp_table:
                if self.arp_table[ip] != mac:
                    print(f"\n[!!!] CRITICAL SECURITY ALERT: DETECTED ARP INCONSISTENCY [!!!]")
                    print(f"    Target IP Interface: {ip} reported a MAC address mutation!")
                    print(f"    Historical Baseline: {self.arp_table[ip]}")
                    print(f"    Anomalous New Entry: {mac} (Potential MitM Spoofing Attack!)")
                    # Update local state mapping to flag ongoing state movements
                    self.arp_table[ip] = mac

if __name__ == "__main__":
    inv = NetworkInventory()

    while True:
        print("\n    1. Scan & Identify Vendors (Active Discovery)")
        print("    2. Start Real-Time ARP Cache Monitor (Defensive Guard)")
        print("    0. Exit")

        choice = input("\n    Select operational path: ")

        if choice == '1':
            target = input("    Enter target network subnet (e.g., 192.168.1.0/24): ")
            inv.scan_and_identify(target)
        elif choice == '2':
            print("[*] Monitoring broadcast pool for dynamic mutations... Press Ctrl+C to terminate.")
            try:
                # store=0 releases evaluated memory immediately
                sniff(filter="arp", prn=inv.monitor_arp_changes, store=0)
            except KeyboardInterrupt:
                print("\n[*] Real-time monitoring session closed by operator.")
        elif choice == '0':
            print("[*] Deactivating database hooks.")
            break
