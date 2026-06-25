import hashlib
import os
import time

class IntegrityMonitor:

    @staticmethod
    def calculate_hash(file_path):
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except FileNotFoundError:
            return None

    def monitor(self, file_path, baseline_hash, interval=5):
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

if __name__ == "__main__":
    target_file = "config_test.txt"
    with open(target_file, "w") as f:
        f.write("SECRET_CONFIG_DATA")

    monitor = IntegrityMonitor()
    baseline = monitor.calculate_hash(target_file)

    print(f"Baseline Hash: {baseline}")
