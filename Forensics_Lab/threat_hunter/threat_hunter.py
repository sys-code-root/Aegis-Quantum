import psutil
import datetime
import time
import ipaddress

class ThreatHunter:
    
    def __init__(self, cpu_threshold=20.0):
        self.cpu_threshold = cpu_threshold

    def scan_processes(self):
        print(f"\n[+] SCANNING PROCESSES (Threshold: {self.cpu_threshold}%)")
        print("-" * 50)

        try:
            processes = list(psutil.process_iter())
            for proc in processes:
                try:
                    proc.cpu_percent()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            time.sleep(0.2)

            for proc in processes:
                try:
                    cpu_usage = proc.cpu_percent()
                    if cpu_usage and cpu_usage > self.cpu_threshold:
                        name = proc.name()
                        pid = proc.pid
                        try:
                            username = proc.username()
                        except psutil.AccessDenied:
                            username = "Access Denied"
                        print(f"    [ALERT] High CPU: {name} (PID: {pid})")
                        print(f"            Usage: {cpu_usage}% | User: {username}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            print(f"[-] Error scanning processes: {e}")

    def scan_network_connections(self):
        print("\n[+] ANALYZING ACTIVE NETWORK CONNECTIONS")
        print("-" * 50)

        try:
            connections = psutil.net_connections(kind='inet')
            for conn in connections:
                if conn.status == 'ESTABLISHED':
                    l_addr = f"{conn.laddr.ip}:{conn.laddr.port}"
                    r_addr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                    remote_ip = conn.raddr.ip if conn.raddr else ""

                    is_external = False
                    if remote_ip:
                        try:
                            ip_obj = ipaddress.ip_address(remote_ip)
                            is_external = not (ip_obj.is_private or ip_obj.is_loopback)
                        except ValueError:
                            is_external = False

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
