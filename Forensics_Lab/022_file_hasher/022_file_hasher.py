import hashlib
import os
import sys

class ForensicFileHasher:

    def __init__(self, file_path):
        self.file_path = file_path

    def generate_hash(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Target artifact not found at provided path: {self.file_path}")

        sha256_hash = hashlib.sha256()
        with open(self.file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        return sha256_hash.hexdigest()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python file_hasher.py <path_to_artifact>")
        sys.exit(1)

    print("\n" + "="*50)
    print("      FORENSIC FILE HASHER (SHA-256)")
    print("="*50)

    target = sys.argv[1]
    hasher = ForensicFileHasher(target)

    print("\n[*] Computing cryptographic DNA fingerprint...")
    try:
        result = hasher.generate_hash()
        print(f"[+] Integrity Signature (SHA-256): {result}")
    except Exception as e:
        print(f"[-] Execution Failure: {e}")
    print("="*50 + "\n")
