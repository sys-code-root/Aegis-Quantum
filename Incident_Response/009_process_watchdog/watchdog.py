import sys
import time
from datetime import datetime
import psutil

class ProcessWatchdog:

    def __init__(self, allowed_processes):
        self.whitelist = {name.lower() for name in allowed_processes}
        self.whitelist.update({"python", "python.exe", "system", "idle"})

    def enforce_policy(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[*] Policy enforcement: {current_time}")

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                name = proc.info['name']
                pid = proc.info['pid']

                if not name:
                    continue

                name = name.lower()

                if pid in (0, 4) or name in ("system", "registry", "smss.exe", "csrss.exe"):
                    continue

                if name not in self.whitelist:
                    print(f"[!] ALERT: Unauthorized process detected: {name} (PID: {pid})")
                    proc.terminate()
                    print(f"[+] SUCCESS: {name} (PID: {pid}) terminated.")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        def start_protection(self, interval=5):
            print("--- WATCHDOG ACTIVE ---")
            try:
                while True:
                    self.enforce_policy()
                    time.sleep(interval)
            except KeyboardInterrupt:
                print("\n[!] Watchdog deactivated.")

if __name__ == "__main__":
    allowed = sys.argv[1:] if len(sys.argv) > 1 else ["cmd.exe", "powershell.exe", "code.exe", "chrome.exe", "explorer.exe", "bash", "zsh"]
    watchdog = ProcessWatchdog(allowed)
    watchdog.start_protection()
