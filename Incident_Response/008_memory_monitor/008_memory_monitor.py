import psutil
import time

class MemoryMonitor:
    """
    Monitors a specific process's memory usage and alerts if it exceeds a threshold.
    Crucial for identifying resource-draining malicious processes or leaks.
    """
    def __init__(self, target_process_name, threshold_mb=100.0):
        self.target_name = target_process_name
        self.threshold_mb = threshold_mb

    def get_process_info(self):
        """Locates process by name and returns its PID and memory in MB."""
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                if self.target_name.lower() in proc.info['name'].lower():
                    # RSS (Resident Set Size) is the actual memory held in RAM
                    rss_mb = proc.info['memory_info'].rss / (1024 * 1024)
                    return proc.info['pid'], rss_mb
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None, None

    def start_monitoring(self, interval=2):
        """Monitors the process in a loop."""
        print(f"[*] Monitoring: {self.target_name} | Threshold: {self.threshold_mb} MB")
        print("-" * 40)

        try:
            while True:
                pid, usage = self.get_process_info()
                if pid:
                    status = "NORMAL" if usage <= self.threshold_mb else "!!! ALERT: HIGH USAGE !!!"
                    print(f"[PID: {pid}] Usage: {usage:.2f} MB | Status: {status}")
                else:
                    print(f"[-] Process '{self.target_name}' not found.")

                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n[!] Monitoring stopped.")

if __name__ == "__main__":
    target = input("Process name to monitor (e.g., chrome): ")
    monitor = MemoryMonitor(target)
    monitor.start_monitoring()
