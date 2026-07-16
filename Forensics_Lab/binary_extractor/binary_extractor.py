import os
import datetime
import binascii
import re
import sys

class BinaryExtractor:
    
    def __init__(self, target_path):
        self.target_path = target_path
        self.file_name = os.path.basename(target_path)

    def get_file_stats(self):
        try:
            stats = os.stat(self.target_path)
            print(f"\n[+] TIMELINE FOR: {self.file_name}")
            print(f"    Access Time: {datetime.datetime.fromtimestamp(stats.st_atime)}")
            print(f"    Modify Time: {datetime.datetime.fromtimestamp(stats.st_mtime)}")
            print(f"    Change Time: {datetime.datetime.fromtimestamp(stats.st_ctime)}")
        except Exception as e:
            print(f"[-] Error retrieving file stats: {e}")

    def verify_header(self):
        signatures = {
            "89504e47": "IMAGE (PNG)",
            "ffd8ffe0": "IMAGE (JPEG)",
            "4d5a": "WINDOWS EXECUTABLE (EXE/DLL)",
            "25504446": "DOCUMENT (PDF)",
            "7f454c46": "LINUX EXECUTABLE (ELF)"
        }
        try:
            with open(self.target_path, "rb") as f:
                header = f.read(4)
                hex_sig = binascii.hexlify(header).decode().lower()

                result = signatures.get(hex_sig, signatures.get(hex_sig[:4], "UNKNOWN"))

                print(f"\n[+] HEADER ANALYSIS")
                print(f"    Magic Number: {hex_sig}")
                print(f"    Real Type:    {result}")
        except Exception as e:
            print(f"[-] Error reading header: {e}")

    def extract_strings(self):
        print(f"\n[+] EXTRACTING HUMAN-READABLE STRINGS (TOP 15)")
        try:
            with open(self.target_path, "rb") as f:
                content_bytes = f.read()
                
                found_bytes = re.findall(rb'[a-zA-Z0-9/._-]{4,}', content_bytes)

                if not found_bytes:
                    print("    No strings found.")
                    return

                for b in found_bytes[:15]:
                    print(f"    Found: {b.decode(errors='ignore')}")
        except Exception as e:
            print(f"[-] Error extracting strings: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python binary_extractor.py <path_to_binary>")
        sys.exit(1)

    target_path = sys.argv[1]
    if os.path.exists(target_path):
        extractor = BinaryExtractor(target_path)
        extractor.get_file_stats()
        extractor.verify_header()
        extractor.extract_strings()
    else:
        print("[-] File not found!")