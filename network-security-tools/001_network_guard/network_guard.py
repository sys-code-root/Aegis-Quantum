import socket
import hashlib
import hmac
import base64
import time

class NetworkGuard:

    @staticmethod
    def get_service_fingerprint(host, port):
        try:
            with socket.create_connection((host, port), timeout=3) as sock:
                sock.send(b"HEAD / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
                banner = sock.recv(1024)
                return hashlib.sha1(banner).hexdigest()
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def xor_obfuscate(data, key_char="Z"):
        return "".join(chr(ord(c) ^ ord(key_char)) for c in data)

    @staticmethod
    def generate_hmac_signature(key, message):
        return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()

    @staticmethod
    def verify_packet_integrity(data, received_hash):
        calculated_hash = hashlib.sha256(data.encode()).hexdigest()
        return hmac.compare_digest(calculated_hash, received_hash)

    @staticmethod
    def encode_for_network(data_bytes):
        return base64.b64encode(data_bytes).decode()

if __name__ == "__main__":
    guard = NetworkGuard()

    original = "SECURE_DATA_2026"
    obfuscated = guard.xor_obfuscate(original)
    print(f"Obfuscated: {obfuscated}")
    print(f"Restored: {guard.xor_obfuscate(obfuscated)}")

    msg = "AUTH_ACTION"
    msg_hash = hashlib.sha256(msg.encode()).hexdigest()
    is_valid = guard.verify_packet_integrity(msg, msg_hash)
    print(f"Integrity Valid: {is_valid}")

    print(f"Google Fingerprint: {guard.get_service_fingerprint('google.com', 80)}")
