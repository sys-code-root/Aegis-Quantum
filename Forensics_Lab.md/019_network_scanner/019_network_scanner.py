import sys
from scapy.all import ARP, Ether, srp, ICMP, IP, sr1

class NetworkScanner:
    """
    Performs active network discovery and host probing.
    Utilizes low-level ARP broadcasting and ICMP validation to map live network assets.
    """
    def __init__(self):
        print("[!] Network Scanner Engine Active.")

    def arp_scan(self, ip_range):
        """
        Broadcasts ARP requests across a subnet to map IP addresses to active MAC addresses.
        Crucial for identifying rogue network interfaces.
        """
        print(f"\n[*] Launching Layer 2 ARP Discovery on: {ip_range}")

        # 1. Create Ethernet frame (Layer 2) targeting the hardware broadcast address
        ether_layer = Ether(dst="ff:ff:ff:ff:ff:ff")

        # 2. Create the Address Resolution Protocol payload (Layer 3 mapping target)
        arp_layer = ARP(pdst=ip_range)

        # 3. Stack layers using Scapy's slash operator mechanics
        packet = ether_layer / arp_layer

        try:
            # srp sends and receives packets at Layer 2 (Data Link)
            answered, _ = srp(packet, timeout=2, verbose=False)

            print("\n[+] LIVE DEVICES IDENTIFIED:")
            print("    IP ADDRESS      MAC ADDRESS")
            print("    " + "-" * 35)

            for _, received in answered:
                print(f"    {received.psrc:<15}   {received.hwsrc}")
        except Exception as e:
            print(f"[-] Hardware query execution fault: {e}")

    def icmp_ping(self, target_ip):
        """Sends a manual network layer ICMP Echo Request frame to validate host state."""
        print(f"\n[*] Injecting custom Layer 3 ICMP Probe into: {target_ip}")

        # Formulate explicit IP destination headers stacked with raw ICMP control structures
        packet = IP(dst=target_ip, ttl=64) / ICMP()

        # sr1 sends 1 packet at Layer 3 (Network) and captures the first reply block
        reply = sr1(packet, timeout=2, verbose=False)

        if reply:
            print(f"    [SUCCESS] Destination {target_ip} responded: HOST IS ALIVE")
            print(f"              Origin Source Trace: {reply.src} | Framework Control Type: {reply.type}")
        else:
            print(f"    [FAILURE] No telemetry return block received from {target_ip} (Host offline or dropping ICMP packages)")

if __name__ == "__main__":
    scanner = NetworkScanner()

    while True:
        print("\n    1. ARP Scan (Network Subnet Discovery)")
        print("    2. ICMP Custom Ping (Target Host Probing)")
        print("    0. Exit")

        choice = input("\n    Select tactical option: ")

        if choice == '1':
            target_range = input("    Enter IP Subnet Range (e.g., 192.168.1.0/24): ")
            scanner.arp_scan(target_range)
        elif choice == '2':
            ip = input("    Enter Target IP Endpoint: ")
            scanner.icmp_ping(ip)
        elif choice == '0':
            print("[*] Shutting down reconnaissance scanners.")
            break
