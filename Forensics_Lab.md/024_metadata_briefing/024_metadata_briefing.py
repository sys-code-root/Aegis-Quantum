import os
import time

class MetadataBrief:
    """
    Extracts essential file-system artifacts and metadata signatures.
    Essential for establishing temporal timelines during forensic investigations.
    """
    def __init__(self, file_path):
        self.file_path = file_path

    def get_brief(self):
        """Retrieves and displays the vital stat parameters of an evidence artifact."""
        try:
            if not os.path.exists(self.file_path):
                print("[-] Error: Evidence artifact not found at target location.")
                return

            # os.stat provides low-level metadata directly from the filesystem kernel table
            stats = os.stat(self.file_path)
            size = stats.st_size
            modified = time.ctime(stats.st_mtime)

            # Masking permissions to isolate the standard rwx bits
            perms = oct(stats.st_mode & 0o777)

            print(f"\n[+] FORENSIC METADATA ARTIFACT: {os.path.basename(self.file_path)}")
            print(f"    File Size:     {size} bytes")
            print(f"    Permissions:   {perms} (Octal Mode)")
            print(f"    Last Modified: {modified}")
        except Exception as e:
            print(f"[-] Forensic metadata extraction fault: {e}")

if __name__ == "__main__":
    target = input("Enter path to evidence artifact for metadata analysis: ")
    brief = MetadataBrief(target)
    brief.get_brief()
