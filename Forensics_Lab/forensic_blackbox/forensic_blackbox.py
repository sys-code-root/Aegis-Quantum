import os
import time
import datetime
import hashlib
import psutil

class ForensicBlackbox:
    
    def __init__(self):
        self.evidence_log = "blackbox_evidence.log"
        self.known_mounts = self.get_current_mounts()
        self.last_mtime = 0
        self.start_time = datetime.datetime.now()
        print(f"[*] Blackbox active. Monitoring Terminal History & Storage Mounts...")

    def get_current_mounts(self):
        try:
            return {partition.mountpoint for partition in psutil.disk_partitions(all=True) if partition.mountpoint}
        except Exception as e:
            print(f"[-] Hardware audit failure: {e}")
            return set()

    def log_evidence(self, category, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{category.upper()}] {message}\n"
        with open(self.evidence_log, "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(log_entry.strip())

    def get_file_hash(self, file_path):
        sha = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(4096):
                    sha.update(chunk)
            return sha.hexdigest()
        except (PermissionError, FileNotFoundError):
            return "HASH_ACCESS_ERROR"

    def monitor_terminal_history(self):
        history_path = os.path.expanduser("~/.bash_history")
        if not os.path.exists(history_path):
            return None

        try:
            current_mtime = os.path.getmtime(history_path)
            if current_mtime == self.last_mtime:
                return None
            self.last_mtime = current_mtime

            with open(history_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                return lines[-1].strip() if lines else None
        except Exception:
            return None

    def scan_new_media(self, new_mount):
        self.log_evidence("MEDIA", f"New storage volume interface mapped at: {new_mount}")
        for root, _, files in os.walk(new_mount):
            for name in files:
                if name.startswith('.'):
                    full_path = os.path.join(root, name)
                    f_hash = self.get_file_hash(full_path)
                    self.log_evidence("SUSPICIOUS", f"Hidden file match: {full_path} | Hash: {f_hash}")

    def run(self, polling_interval=3):
        last_cmd = ""
        try:
            while True:
                current_cmd = self.monitor_terminal_history()
                if current_cmd and current_cmd != last_cmd:
                    self.log_evidence("COMMAND", current_cmd)
                    last_cmd = current_cmd

                current_mounts = self.get_current_mounts()
                new_parts = current_mounts - self.known_mounts

                if new_parts:
                    for part in new_parts:
                        self.scan_new_media(part)
                
                self.known_mounts = current_mounts
                time.sleep(polling_interval)
        except KeyboardInterrupt:
            self.log_evidence("SYSTEM", "Observational forensic tracking stopped by operator.")

if __name__ == "__main__":
    print("-" * 50)
    print("PYTHON FORENSIC BLACKBOX v1.0")
    print("Tracking Target Context: Bash Traces & External Medium Mounts")
    print("-" * 50)

    blackbox = ForensicBlackbox()
    blackbox.run()
