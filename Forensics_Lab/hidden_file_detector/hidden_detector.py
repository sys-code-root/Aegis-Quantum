import os
import sys

class HiddenFileDetector:

    def __init__(self, target_dir):
        self.target_dir = target_dir

    def scan(self):
        if not os.path.isdir(self.target_dir):
            print(f"[-] Error: Specified directory context not found: {self.target_dir}")
            return

        print(f"[*] Initiating triage scan for hidden items in: {self.target_dir}\n")
        hidden_count = 0

        try:
            for root, dirs, files in os.walk(self.target_dir):
                for d in dirs:
                    if d.startswith('.'):
                        full_path = os.path.join(root, d)
                        print(f"    [DIR]  Hidden: {full_path}")
                        hidden_count += 1

                for file in files:
                    if file.startswith('.'):
                        full_path = os.path.join(root, file)
                        print(f"    [FILE] Hidden: {full_path}")
                        hidden_count += 1

            print(f"\n[+] Triage complete. Total hidden filesystem artifacts located: {hidden_count}")
        except Exception as e:
            print(f"[-] Forensic scanning fault: {e}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    detector = HiddenFileDetector(target)
    detector.scan()
