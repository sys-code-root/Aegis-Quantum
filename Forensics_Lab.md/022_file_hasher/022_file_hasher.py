import hashlib
import os

class ForensicFileHasher:
    """
    Generates cryptographic fingerprints (SHA-256) for digital evidence.
    Establishes the immutable baseline for chain-of-custody verification.
    """
    def __init__(self, file_path):
        self.file_path = file_path

    def generate_hash(self):
        """
        Reads the target file in buffered blocks to ensure memory efficiency 
        and computes a SHA-256 integrity signature.
        """
        sha256_hash = hashlib.sha256()

        try:
            if not os.path.exists(self.file_path):
                return "[-] Error: Target artifact not found at provided path."

            with open(self.file_path, "rb") as f:
                # Buffering in 4KB chunks ensures stability for multi-gigabyte forensic images
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)

            return sha256_hash.hexdigest()
        except Exception as e:
            return f"[-] Cryptographic hashing fault: {e}"

if __name__ == "__main__":
    print("\n" + "="*50)
    print("      FORENSIC FILE HASHER (SHA-256)")
    print("="*50)

    target = input("Enter path to forensic evidence artifact: ")
    hasher = ForensicFileHasher(target)

    print("\n[*] Computing cryptographic DNA fingerprint...")
    result = hasher.generate_hash()
    print(f"[+] Integrity Signature (SHA-256): {result}")
    print("="*50 + "\n")
