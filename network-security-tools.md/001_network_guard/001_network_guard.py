import socket
import hashlib
import hmac
import base64
import time

class NetworkGuard:
    """
    A utility class for network integrity verification and simple obfuscation.
    """

    @staticmethod
    def get_service_fingerprint(host, port):
        """Fetches a service banner and returns its SHA-1 hash."""
        try:
            with socket.create_connection((host, port), timeout=3) as sock:
                sock.send(b"HEAD / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
                banner = sock.recv(1024)
                return hashlib.sha1(banner).hexdigest()
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def xor_obfuscate(data, key_char="Z"):
        """Performs a simple XOR obfuscation on a string."""
        return "".join(chr(ord(c) ^ ord(key_char)) for c in data)

    @staticmethod
    def generate_hmac_signature(key, message):
        """Generates an HMAC-SHA256 signature for message authentication."""
        return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()

    @staticmethod
    def verify_packet_integrity(data, received_hash):
        """Verifies if the data matches the provided SHA-256 hash."""
        calculated_hash = hashlib.sha256(data.encode()).hexdigest()
        return hmac.compare_digest(calculated_hash, received_hash)

    @staticmethod
    def encode_for_network(data_bytes):
        """Encodes raw bytes to base64 for safe network transmission."""
        return base64.b64encode(data_bytes).decode()

# Example usage
if __name__ == "__main__":
    guard = NetworkGuard()

    # 1. Obfuscation Example
    original = "SECURE_DATA_2026"
    obfuscated = guard.xor_obfuscate(original)
    print(f"Obfuscated: {obfuscated}")
    print(f"Restored: {guard.xor_obfuscate(obfuscated)}")

    # 2. Integrity Example
    msg = "AUTH_ACTION"
    msg_hash = hashlib.sha256(msg.encode()).hexdigest()
    is_valid = guard.verify_packet_integrity(msg, msg_hash)
    print(f"Integrity Valid: {is_valid}")

    # 3. Network Fingerprint
    print(f"Google Fingerprint: {guard.get_service_fingerprint('google.com', 80)}")
