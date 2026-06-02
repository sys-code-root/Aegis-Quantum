from scapy.all import sniff, IP, TCP
from collections import defaultdict

class NetworkFlowAnalyzer:
    """
    Analyzes network traffic in real-time to identify high-volume data flows.
    Essential for detecting data exfiltration or suspicious communication patterns.
    """
    def __init__(self):
        # Key: (Source_IP, Dest_IP, Dest_Port) | Value: Total Bytes
        self.flows = defaultdict(int)

    def _packet_callback(self, packet):
        """Processes and tracks packet payload volume."""
        if packet.haslayer(IP) and packet.haslayer(TCP):
            src = packet[IP].src
            dst = packet[IP].dst
            port = packet[TCP].dport
            size = len(packet[TCP].payload)

            if size > 0:
                self.flows[(src, dst, port)] += size
                print(f"[+] Traffic: {src} -> {dst}:{port} | +{size} bytes")

    def start_sniffing(self, interface=None, count=50):
        """Starts packet capture on a specified interface."""
        print(f"[*] Sniffing {count} packets on {interface or 'default interface'}...")
        try:
            sniff(iface=interface, prn=self._packet_callback, count=count, store=0)
            self.generate_report()
        except PermissionError:
            print("[-] Error: Insufficient privileges. Run as Administrator/Root.")

    def generate_report(self):
        """Displays a summary of top traffic flows."""
        print("\n" + "="*50 + "\nNETWORK TRAFFIC SUMMARY\n" + "="*50)
        sorted_flows = sorted(self.flows.items(), key=lambda x: x[1], reverse=True)
        for (src, dst, port), size in sorted_flows:
            print(f"Flow: {src} -> {dst}:{port} | Total: {size} bytes")

if __name__ == "__main__":
    analyzer = NetworkFlowAnalyzer()
    analyzer.start_sniffing(count=50)
