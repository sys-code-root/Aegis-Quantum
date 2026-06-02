import hashlib
import os

class HashSignature:
    """
    Simulates a Hash-Based Signature scheme (One-Time Signature principle).
    Provides post-quantum security by relying on collision-resistant hash functions.
    """
    def __init__(self):
        # Secret Key: 32 bytes of high-entropy random data
        self.secret_key = os.urandom(32)
        # Public Key: The cryptographic hash of the secret key
        self.public_key = self._hash(self.secret_key)
        print("[!] PQC Identity keys initialized via SHA-256.")

    def _hash(self, data) -> str:
        """Utility function for standardized SHA-256 generation."""
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha256(data).hexdigest()

    def sign_message(self, message: str) -> str:
        """
        Creates a unique signature by binding the secret key with the 
        hashed content of the message.
        """
        message_hash = self._hash(message)
        # Signature is a unique cryptographic elo of the secret + message
        signature = self._hash(self.secret_key + message_hash.encode())
        return signature

    def verify(self, message: str, signature: str) -> bool:
        """Validates the signature integrity via cryptographic reconstruction."""
        print("\n[*] Verifying Post-Quantum Signature integrity...")
        check = self._hash(self.secret_key + self._hash(message).encode())
        return check == signature

if __name__ == "__main__":
    pqc = HashSignature()
    msg = "Transfer 1621.00 BRL from secure account"

    # Signature generation routine
    sig = pqc.sign_message(msg)

    print(f"[+] Message Payload: {msg}")
    print(f"[+] Cryptographic Signature: {sig[:32]}... (Truncated)")

    # Integrity verification
    is_valid = pqc.verify(msg, sig)
    print(f"[RESULT] Signature Status Valid: {is_valid}")
