import os
import time
import datetime
import hashlib
import psutil

class ForensicBlackbox:
    """
    Monitors host behavioral infrastructure inside Linux/WSL.
    Tracks live command executions via shell histories and cross-references hardware 
    mountpoints to analyze dynamic external storage media insertions.
    """
    def __init__(self):
        self.evidence_log = "blackbox_evidence.log"
        self.known_mounts = self.get_current_mounts()
        self.start_time = datetime.datetime.now()
        print(f"[*] Blackbox active. Monitoring Terminal History & Storage Mounts...")

    def get_current_mounts(self):
        """Queries the system partition tables to fetch active partition mount points."""
        try:
            return {partition.mountpoint for partition in psutil.disk_partitions()}
        except Exception as e:
            print(f"[-] Hardware audit failure: {e}")
            return set()

    def log_evidence(self, category, message):
        """Writes strictly timestamped events to the central forensic log file."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{category.upper()}] {message}\n"
        with open(self.evidence_log, "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(log_entry.strip())

    def get_file_hash(self, file_path):
        """Generates a cryptographic SHA-256 hash to seal newly discovered file artifacts."""
        sha = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(4096):
                    sha.update(chunk)
            return sha.hexdigest()
        except (PermissionError, FileNotFoundError):
            return "HASH_ACCESS_ERROR"

    def monitor_terminal_history(self):
        """Parses the active shell profile history to catch real-time input traces."""
        history_path = os.path.expanduser("~/.bash_history")
        if not os.path.exists(history_path):
            return None

        try:
            with open(history_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                return lines[-1].strip() if lines else None
        except Exception:
            return None

    def scan_new_media(self, new_mount):
        """Performs immediate targeted triage on newly attached storage volumes."""
        self.log_evidence("MEDIA", f"New storage volume interface mapped at: {new_mount}")
        for root, _, files in os.walk(new_mount):
            for name in files:
                # Prioritize scanning hidden files often used to conceal scripts or payloads
                if name.startswith('.'):
                    full_path = os.path.join(root, name)
                    f_hash = self.get_file_hash(full_path)
                    self.log_evidence("SUSPICIOUS", f"Hidden file match: {full_path} | Hash: {f_hash}")

    def run(self, polling_interval=3):
        """Enforces continuous host behavior monitoring loops."""
        last_cmd = ""
        try:
            while True:
                # 1. Audit Shell Actions
                current_cmd = self.monitor_terminal_history()
                if current_cmd and current_cmd != last_cmd:
                    self.log_evidence("COMMAND", current_cmd)
                    last_cmd = current_cmd

                # 2. Audit Volume Montages
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
