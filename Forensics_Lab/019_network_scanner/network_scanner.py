import sys
from scapy.all import ARP, Ether, srp, ICMP, IP, sr1

class NetworkScanner:

    def __init__(self):
        print("[!] Network Scanner Engine Active.")

    def arp_scan(self, ip_range):
        if not ip_range.strip():
            print("[-] Error: IP range cannot be empty.")
            return

        print(f"\n[*] Launching Layer 2 ARP Discovery on: {ip_range}")
        packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range)

        try:
            answered, _ = srp(packet, timeout=2, verbose=False)

            print("\n[+] LIVE DEVICES IDENTIFIED:")
            print("    IP ADDRESS       MAC ADDRESS")
            print("    " + "-" * 35)

            for _, received in answered:
                print(f"    {received.psrc:<15}   {received.hwsrc}")
        except KeyboardInterrupt:
            print("\n[!] ARP scan scan interrupted by operator.")
        except Exception as e:
            print(f"[-] Hardware query execution fault: {e}")

    def icmp_ping(self, target_ip):
        if not target_ip.strip():
            print("[-] Error: Target IP cannot be empty.")
            return

        print(f"\n[*] Injecting custom Layer 3 ICMP Probe into: {target_ip}")
        packet = IP(dst=target_ip, ttl=64) / ICMP()

        try:
            reply = sr1(packet, timeout=2, verbose=False)

            if reply:
                print(f"    [SUCCESS] Destination {target_ip} responded: HOST IS ALIVE")
                print(f"              Origin Source Trace: {reply.src}")
            else:
                print(f"    [FAILURE] No telemetry return block received from {target_ip}")
        except KeyboardInterrupt:
            print("\n[!] ICMP probe interrupted by operator.")
        except Exception as e:
            print(f"[-] Execution Failure: {e}")

if __name__ == "__main__":
    scanner = NetworkScanner()

    while True:
        print("\n    1. ARP Scan (Network Subnet Discovery)")
        print("    2. ICMP Custom Ping (Target Host Probing)")
        print("    0. Exit")

        try:
            choice = input("\n    Select tactical option: ")

            if choice == '1':
                target_range = input("    Enter IP Subnet Range (e.g., 192.168.1.0/24): ")
                scanner.arp_scan(target_range)
            elif choice == '2':
                ip = input("    Enter Target IP Endpoint: ")
                scanner.icmp_ping(ip)
            elif choice == '0':
                print("[*] Shutting down reconnaissance scanners.")
                sys.exit(0)
            else:
                print("[-] Invalid selection. Please try again.")
        except KeyboardInterrupt:
            print("\n[*] Shutting down reconnaissance scanners.")
            sys.exit(0)
