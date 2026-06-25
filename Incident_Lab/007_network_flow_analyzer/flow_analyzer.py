import sys
from scapy.all import sniff, IP, TCP
from collections import defaultdict

class NetworkFlowAnalyzer:

    def __init__(self):
        self.flows = defaultdict(int)

    def _packet_callback(self, packet):
        if packet.haslayer(IP) and packet.haslayer(TCP):
            src = packet[IP].src
            dst = packet[IP].dst
            port = packet[TCP].dport
            size = len(packet)

            self.flows[(src, dst, port)] += size
            print(f"[+] Traffic: {src} -> {dst}:{port} | +{size} bytes")

    def start_sniffing(self, interface=None, count=50):
        print(f"[*] Sniffing {count} packets on {interface or 'all interfaces'}...")
        try:
            sniff(iface=interface, prn=self._packet_callback, count=count, store=0)
            self.generate_report()
        except Exception as e:
            print(f"[-] Execution Failure: {e}")
            print("[-] Ensure the script is running with elevated administrative/root privileges.")

    def generate_report(self):
        print("\n" + "="*50 + "\nNETWORK TRAFFIC SUMMARY\n" + "="*50)
        sorted_flows = sorted(self.flows.items(), key=lambda x: x[1], reverse=True)
        for (src, dst, port), size in sorted_flows:
            print(f"Flow: {src} -> {dst}:{port} | Total: {size} bytes")

if __name__ == "__main__":
    pkt_count = 50
    iface = None

    if len(sys.argv) > 1:
        if sys.argv[1] in ("-h", "--help"):
            print("Usage: python flow_analyzer.py [count] [interface]")
            sys.exit(0)
        if sys.argv[1].isdigit():
            pkt_count = int(sys.argv[1])
            if len(sys.argv) > 2:
                iface = sys.argv[2]
        else:
            iface = sys.argv[1]
            if len(sys.argv) > 2 and sys.argv[2].isdigit():
                pkt_count = int(sys.argv[2])

    analyzer = NetworkFlowAnalyzer()
    analyzer.start_sniffing(interface=iface, count=pkt_count)
