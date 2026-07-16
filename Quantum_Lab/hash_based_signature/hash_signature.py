import hashlib
import os

class HashSignature:
    def __init__(self):
        self.secret_key = os.urandom(32)
        self.public_key = self._hash(self.secret_key)
        print("[!] PQC Identity keys initialized via SHA-256.")

    def _hash(self, data) -> str:
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha256(data).hexdigest()

    def sign_message(self, message: str) -> str:
        message_hash = self._hash(message)
        signature = self._hash(self.secret_key + message_hash.encode())
        return signature

    def verify(self, message: str, signature: str) -> bool:
        print("\n[*] Verifying Post-Quantum Signature integrity...")
        check = self._hash(self.secret_key + self._hash(message).encode())
        return check == signature

if __name__ == "__main__":
    pqc = HashSignature()
    msg = "Transfer 1621.00 BRL from secure account"

    sig = pqc.sign_message(msg)

    print(f"[+] Message Payload: {msg}")
    print(f"[+] Cryptographic Signature: {sig[:32]}... (Truncated)")

    is_valid = pqc.verify(msg, sig)
    print(f"[RESULT] Signature Status Valid: {is_valid}")
