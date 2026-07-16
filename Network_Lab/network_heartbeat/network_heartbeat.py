import socket
import hashlib
import time
import secrets

class NetworkHeartbeat:

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def generate_heartbeat(self):
        timestamp = str(int(time.time()))
        raw_data = f"{timestamp}{self.secret_key}".encode()
        auth_hash = hashlib.sha256(raw_data).hexdigest()
        return f"{timestamp}:{auth_hash}"

    @staticmethod
    def verify_heartbeat(packet, secret_key, window_seconds=5):
        try:
            timestamp, received_hash = packet.split(":")
            current_time = int(time.time())

            if abs(current_time - int(timestamp)) > window_seconds:
                return False, "Expired Heartbeat"
            
            expected_data = f"{timestamp}{secret_key}".encode()
            expected_hash = hashlib.sha256(expected_data).hexdigest()

            if secrets.compare_digest(expected_hash, received_hash):
                return True, "Valid"
            return False, "Tampered Data"

        except Exception:
            return False, "Invalid Format"

if __name__ == "__main__":
    key = "APOLO_11_2026_SECRET"
    hb_manager = NetworkHeartbeat(key)

    packet = hb_manager.generate_heartbeat()
    print(f"Generated Packet: {packet}")

    is_valid, status = NetworkHeartbeat.verify_heartbeat(packet, key)
    print(f"Status: {status} | Valid: {is_valid}")
