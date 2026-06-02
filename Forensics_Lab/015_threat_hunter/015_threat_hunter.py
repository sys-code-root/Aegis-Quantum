import psutil
import datetime

class ThreatHunter:
    """
    Performs live forensics to detect volatile indicators of compromise (IoCs).
    Scans for high-CPU rogue processes (miners) and untrusted external network connections.
    """
    def __init__(self, cpu_threshold=20.0):
        self.cpu_threshold = cpu_threshold
        # RFC 1918 and local loopback prefixes to filter internal traffic
        self.local_prefixes = ("127.", "192.168.", "10.", "172.")

    def scan_processes(self):
        """Audits the process table to flag high resource consumption."""
        print(f"\n[+] SCANNING PROCESSES (Threshold: {self.cpu_threshold}%)")
        print("-" * 50)

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'username']):
            try:
                cpu_usage = proc.info['cpu_percent']
                # psutil can return None for CPU percent on initial check windows
                if cpu_usage and cpu_usage > self.cpu_threshold:
                    print(f"    [ALERT] High CPU: {proc.info['name']} (PID: {proc.info['pid']})")
                    print(f"            Usage: {cpu_usage}% | User: {proc.info['username']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def scan_network_connections(self):
        """Inspects active network sockets to flag unverified external endpoints."""
        print("\n[+] ANALYZING ACTIVE NETWORK CONNECTIONS")
        print("-" * 50)

        try:
            connections = psutil.net_connections(kind='inet')
            for conn in connections:
                if conn.status == 'ESTABLISHED':
                    l_addr = f"{conn.laddr.ip}:{conn.laddr.port}"
                    r_addr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                    remote_ip = conn.raddr.ip if conn.raddr else ""

                    # Identify if destination ip falls outside corporate/local boundaries
                    is_external = remote_ip and not remote_ip.startswith(self.local_prefixes)
                    status = "[EXTERNAL]" if is_external else "[INTERNAL]"

                    print(f"    {status:<10} {l_addr} --> {r_addr}")
        except psutil.AccessDenied:
            print("[-] Error: Insufficient privileges to audit network sockets. Run as Root/Admin.")

if __name__ == "__main__":
    hunter = ThreatHunter()
    print(f"[*] Threat Hunter Live Forensics Session Started: {datetime.datetime.now()}")

    hunter.scan_processes()
    hunter.scan_network_connections()

    print("\n[+] Audit Complete.")
