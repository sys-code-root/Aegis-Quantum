import sys
import time
import psutil

class MemoryMonitor:

    def __init__(self, target_process_name, threshold_mb=100.0):
        self.target_name = target_process_name.lower()
        self.threshold_mb = threshold_mb
        self._cached_process = None

    def _fetch_process_instance(self):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if self.target_name in proc.info['name'].lower():
                    self._cached_process = psutil.Process(proc.info['pid'])
                    return self._cached_process
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None

    def start_monitoring(self, interval=2):
        print(f"[*] Monitoring: {self.target_name} | Threshold: {self.threshold_mb} MB")
        print("-" * 50)

        try:
            while True:
                proc = self._cached_process or self._fetch_process_instance()

                if proc:
                    try:
                        rss_mb = proc.memory_info().rss / (1024 ** 2)
                        status = "NORMAL" if rss_mb <= self.threshold_mb else "!!! ALERT: HIGH USAGE !!!"
                        print(f"[PID: {proc.pid}] Usage: {rss_mb:.2f} MB | Status: {status}")
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        print(f"[-] Process instance (PID: {proc.pid}) terminated. Re-scanning...")
                        self._cached_process = None
                else:
                    print(f"[-] Active instance for target '{self.target_name}' not found.")

                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n[!] Monitoring session stopped by operator.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python memory_monitor.py <process_name> [threshold_mb]")
        sys.exit(1)

    target_name = sys.argv[1]
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 100.0

    monitor = MemoryMonitor(target_name, threshold)
    monitor.start_monitoring()
