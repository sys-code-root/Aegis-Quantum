import os
import sys
import datetime

class MetadataBrief:

    def __init__(self, file_path):
        self.file_path = file_path

    def get_brief(self):
        try:
            stats = os.stat(self.file_path)
            size = stats.st_size
            modified = datetime.datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            perms = f"{stats.st_mode & 0o777:03o}"

            print(f"\n[+] FORENSIC METADATA ARTIFACT: {os.path.basename(self.file_path)}")
            print(f"    File Size:     {size} bytes")
            print(f"    Permissions:   {perms} (Octal Mode)")
            print(f"    Last Modified: {modified}")
        except FileNotFoundError:
            print(f"[-] Error: Evidence artifact not found at target location: {self.file_path}")
        except PermissionError:
            print(f"[-] Error: Insufficient privileges to read metadata for: {self.file_path}")
        except Exception as e:
            print(f"[-] Forensic metadata extraction fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python metadata_brief.py <path_to_artifact>")
        sys.exit(1)

    brief = MetadataBrief(sys.argv[1])
    brief.get_brief()
