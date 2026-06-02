import os
import datetime
import binascii
import re

class BinaryExtractor:
    """
    Performs static forensic analysis on binary files.
    Extracts MAC timelines, verifies magic number headers, and isolates
    human-readable strings to discover indicators of compromise (IoCs).
    """
    def __init__(self, target_path):
        self.target_path = target_path
        self.file_name = os.path.basename(target_path)

    def get_file_stats(self):
        """Extracts MAC (Modified, Accessed, Created) timeline from the filesystem."""
        try:
            stats = os.stat(self.target_path)
            print(f"\n[+] TIMELINE FOR: {self.file_name}")
            print(f"    Access Time: {datetime.datetime.fromtimestamp(stats.st_atime)}")
            print(f"    Modify Time: {datetime.datetime.fromtimestamp(stats.st_mtime)}")
            print(f"    Change Time: {datetime.datetime.fromtimestamp(stats.st_ctime)}")
        except Exception as e:
            print(f"[-] Error retrieving file stats: {e}")

    def verify_header(self):
        """Validates file type using hexadecimal magic numbers to catch extension spoofing."""
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

                # Check 4 bytes first, fallback to 2 bytes if needed (like 4d5a)
                result = signatures.get(hex_sig, signatures.get(hex_sig[:4], "UNKNOWN"))

                print(f"\n[+] HEADER ANALYSIS")
                print(f"    Magic Number: {hex_sig}")
                print(f"    Real Type:    {result}")
        except Exception as e:
            print(f"[-] Error reading header: {e}")

    def extract_strings(self):
        """Extracts ASCII strings of 4 or more characters from the raw binary content."""
        print(f"\n[+] EXTRACTING HUMAN-READABLE STRINGS (TOP 15)")
        try:
            with open(self.target_path, "rb") as f:
                content = f.read().decode(errors='ignore')
                # Regex looks for alphanumeric or basic punctuation strings (minimum length: 4)
                found_strings = re.findall(r'[a-zA-Z0-9/._-]{4,}', content)

                if not found_strings:
                    print("    No strings found.")
                    return

                for s in found_strings[:15]:
                    print(f"    Found: {s}")
        except Exception as e:
           print(f"[-] Error extracting strings: {e}")

if __name__ == "__main__":
    path = input("Enter the full path of the file: ")
    if os.path.exists(path):
        extractor = BinaryExtractor(path)
        extractor.get_file_stats()
        extractor.verify_header()
        extractor.extract_strings()
    else:
        print("[-] File not found!")
