import hashlib
import os
import time

class IntegrityMonitor:
    """
    Monitors a file for unauthorized changes using SHA-256 hashing.
    Useful for system configuration audits and identifying tampered logs.
    """

    @staticmethod
    def calculate_hash(file_path):
        """Calculates the SHA-256 hash of a file's content."""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                # Read in chunks to handle large files efficiently
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except FileNotFoundError:
            return None

    def monitor(self, file_path, baseline_hash, interval=5):
        """Continuously monitors a file against a known-good hash."""
        print(f"Monitoring: {file_path}...")
        try:
            while True:
                current_hash = self.calculate_hash(file_path)
                if current_hash != baseline_hash:
                    print(f"[!] ALERT: File integrity compromised! Hash mismatch.")
                    break
                print(f"[*] Integrity verified at {time.strftime('%H:%M:%S')}")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user.")

# Example Usage
if __name__ == "__main__":
    # Create a dummy file for demonstration
    target_file = "config_test.txt"
    with open(target_file, "w") as f:
        f.write("SECRET_CONFIG_DATA")

    monitor = IntegrityMonitor()
    baseline = monitor.calculate_hash(target_file)

    print(f"Baseline Hash: {baseline}")
    # monitor.monitor(target_file, baseline) # Uncomment to start continuous monitoring
