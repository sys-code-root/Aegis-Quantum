import os
import time
import hashlib
import datetime

class SentinelWatchdog:
    """
    File Integrity Monitor (FIM) for real-time directory auditing.
    Tracks file creations, modifications, and deletions using SHA-256 cryptographic hashes.
    """
    def __init__(self, directory_to_watch):
        self.directory = directory_to_watch
        self.snapshot = {}  # Format: {file_path: sha256_hash}
        self.log_file = "sentinel_audit.log"
        print(f"[!] Sentinel active on: {self.directory}")

    def calculate_hash(self, file_path):
        """Generates a SHA-256 hash to verify physical file integrity."""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                # 4KB blocks process large forensic targets efficiently without RAM spikes
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except (PermissionError, FileNotFoundError):
            return None

    def log_event(self, event_type, details):
        """Records state modifications to console and secure historical log."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{event_type.upper()}] {details}"
        print(entry)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(entry + "\n")

    def take_snapshot(self):
        """Captures a baseline state matrix of all target directory trees."""
        current_files = {}
        for root, _, files in os.walk(self.directory):
            for name in files:
                full_path = os.path.join(root, name)
                f_hash = self.calculate_hash(full_path)
                if f_hash:  # Only index accessible records
                    current_files[full_path] = f_hash
        return current_files

    def start_monitoring(self, interval=2):
        """Executes the main recursive audit validation loop."""
        self.snapshot = self.take_snapshot()
        print("[*] Initial snapshot complete. Monitoring for structural mutations...")

        try:
            while True:
                time.sleep(interval)
                current_state = self.take_snapshot()

                # 1. Delta check for new or modified records
                for path, file_hash in current_state.items():
                    if path not in self.snapshot:
                        status = "HIDDEN" if os.path.basename(path).startswith('.') else "NEW"
                        self.log_event(status, f"File path: {path} | Hash: {file_hash}")
                    elif self.snapshot[path] != file_hash:
                        self.log_event("MODIFIED", f"Content changed: {path} | New Hash: {file_hash}")

                # 2. Delta check for deleted paths
                for path in self.snapshot:
                    if path not in current_state:
                        self.log_event("DELETED", f"Resource purged: {path}")

                self.snapshot = current_state
        except KeyboardInterrupt:
            print("\n[!] Sentinel deactivated. Review sentinel_audit.log for captured sequences.")

if __name__ == "__main__":
    target = input("Enter directory context path to monitor: ")
    if os.path.isdir(target):
        watchdog = SentinelWatchdog(target)
        watchdog.start_monitoring()
    else:
        print("[-] Error: Specified baseline target is not a valid filesystem directory.")
