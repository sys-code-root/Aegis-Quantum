import os

class HiddenFileDetector:
    """
    Performs forensic triage to expose hidden files and directories.
    Targets files masked by the '.' dotfile convention common in Linux/WSL.
    """
    def __init__(self, target_dir):
        self.target_dir = target_dir

    def scan(self):
        """Recursively scans the directory to identify hidden filesystem artifacts."""
        print(f"[*] Initiating triage scan for hidden items in: {self.target_dir}\n")

        try:
            items = os.listdir(self.target_dir)
            hidden_count = 0

            for item in items:
                # Identification logic: '.' prefix mask is the standard Linux hiding convention
                if item.startswith('.'):
                    print(f"    [FOUND] Hidden Artifact: {item}")
                    hidden_count += 1

            print(f"\n[+] Triage complete. Total hidden filesystem artifacts located: {hidden_count}")
        except Exception as e:
            print(f"[-] Forensic scanning fault: {e}")

if __name__ == "__main__":
    path = input("Enter directory context for hidden item scan (default is '.'): ") or "."
    if os.path.isdir(path):
        detector = HiddenFileDetector(path)
        detector.scan()
    else:
        print("[-] Error: Specified directory context not found.")
