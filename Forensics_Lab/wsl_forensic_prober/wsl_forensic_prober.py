import binascii
import datetime
import os
import platform
import time
import psutil

class WSLForensicProber:
    
    def __init__(self):
        self.log_file = "wsl_forensic_evidence.log"
        self.signatures = {
            "89504e47": "PNG Image",
            "ffd8ffe0": "JPEG Image",
            "25504446": "PDF Document",
            "4d5a": "Windows Executable",
            "7f454c46": "Linux ELF Executable",
            "504b0304": "ZIP/Office Doc"
        }

    def write_log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message}"
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
        print(f"[*] {message}")

    def analyze_file_integrity(self, path):
        if not os.path.exists(path):
            self.write_log(f"ALERT: Path not found: {path}")
            return

        stat = os.stat(path)
        self.write_log(f"File: {os.path.basename(path)}")
        self.write_log(f"|-- Created: {datetime.datetime.fromtimestamp(stat.st_ctime)}")
        self.write_log(f"|-- Modified: {datetime.datetime.fromtimestamp(stat.st_mtime)}")

        try:
            with open(path, "rb") as f:
                header = binascii.hexlify(f.read(4)).decode().lower()
                
                detected_type = "Unknown"
                for sig, label in self.signatures.items():
                    if header.startswith(sig):
                        detected_type = label
                        break
                        
                self.write_log(f"|-- Signature: {detected_type} ({header})")
        except Exception as e:
            self.write_log(f"|-- Error reading header: {e}")

    def audit_system_resources(self, cpu_threshold=20.0):
        self.write_log("Starting WSL/Linux process audit...")
        
        psutil.cpu_percent(interval=None)
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                cpu = proc.cpu_percent(interval=0.01)
                if cpu and cpu > cpu_threshold:
                    self.write_log(f"HIGH CPU: {proc.info['name']} (PID {proc.info['pid']}) - {cpu}%")
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                continue

    def check_persistence(self):
        paths = [os.path.expanduser("~/.bashrc"), os.path.expanduser("~/.profile"), "/etc/rc.local"]
        for path in paths:
            if os.path.exists(path):
                with open(path, "r", errors="ignore") as f:
                    content = f.read()
                    if any(cmd in content for cmd in ["http", "curl", "nc"]):
                        self.write_log(f"[!] Warning: Suspicious network commands in {path}")

    def monitor_folder_realtime(self, path, limit=5):
        self.write_log(f"Monitoring {path} for {limit}s...")
        start = time.time()
        initial_files = set(os.listdir(path))

        while time.time() - start < limit:
            current_files = set(os.listdir(path))
            if current_files != initial_files:
                added = current_files - initial_files
                removed = initial_files - current_files
                if added: self.write_log(f"ADDED: {added}")
                if removed: self.write_log(f"REMOVED: {removed}")
                initial_files = current_files
            time.sleep(1)

if __name__ == "__main__":
    print(f"--- 012_WSL_FORENSIC_PROBER | OS: {platform.system()} ---")
    prober = WSLForensicProber()
    
    prober.check_persistence()
    
    prober.audit_system_resources()
    
    test_path = "wsl_forensic_evidence.log" 
    prober.analyze_file_integrity(test_path)
    
    prober.monitor_folder_realtime(".", limit=5)