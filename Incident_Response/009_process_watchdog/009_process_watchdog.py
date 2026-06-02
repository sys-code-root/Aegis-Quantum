import psutil
import time

class ProcessWatchdog:
    """
    Enforces a process whitelist policy by automatically terminating 
    unauthorized processes. Useful for securing forensic workstations 
    or focus environments.
    """
    def __init__(self, allowed_processes):
        self.whitelist = [name.lower() for name in allowed_processes]
        # Always protect the Python interpreter to keep the watchdog alive
        self.whitelist.extend(["python", "python.exe"])

    def enforce_policy(self):
        """Scans running processes and kills those not in the whitelist."""
        print(f"[*] Policy enforcement: {time.ctime()}")

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                name = proc.info['name'].lower()
                pid = proc.info['pid']

                # Filter out critical system processes (PID < 100 on Windows)
                if pid < 100:
                    continue

                if name not in self.whitelist:
                    print(f"[!] ALERT: Unauthorized process detected: {name} (PID: {pid})")
                    p = psutil.Process(pid)
                    p.terminate()
                    print(f"[+] SUCCESS: {name} (PID: {pid}) terminated.")

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    def start_protection(self, interval=10):
        """Starts the watchdog in a continuous loop."""
        print("--- WATCHDOG ACTIVE ---")
        try:
            while True:
                self.enforce_policy()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n[!] Watchdog deactivated.")

if __name__ == "__main__":
    # Define authorized apps for your specific study/work context
    my_allowed = ["cmd.exe", "powershell.exe", "code.exe", "chrome.exe", "explorer.exe"]
    watchdog = ProcessWatchdog(my_allowed)
    watchdog.start_protection()
