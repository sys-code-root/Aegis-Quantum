import socket
import hashlib
import time
import secrets

class NetworkHeartbeat:
    """
    Generates and verifies secure heartbeats to prevent Replay Attacks
    and ensure device availability in a network.
    """

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def generate_heartbeat(self):
        """
        Creates a time-sensitive packet with an HMAC-like hash.
        The packet is valid only for a specific window (current time).
        """
        timestamp = str(int(time.time()))
        # Combine timestamp with secret to ensure uniqueness per second
        raw_data = f"{timestamp}{self.secret_key}".encode()
        auth_hash = hashlib.sha256(raw_data).hexdigest()

        return f"{timestamp}:{auth_hash}"

    @staticmethod
    def verify_heartbeat(packet, secret_key, window_seconds=5):
        """
        Verifies if the heartbeat is authentic and within the time window.
        """
        try:
            timestamp, received_hash = packet.split(":")
            current_time = int(time.time())

            # Check if timestamp is within the allowed window
            if abs(current_time - int(timestamp)) > window_seconds:

                return False, "Expired Heartbeat"
            # Recalculate hash to verify integrity
            expected_data = f"{timestamp}{secret_key}".encode()
            expected_hash = hashlib.sha256(expected_data).hexdigest()

            if secrets.compare_digest(expected_hash, received_hash):
                return True, "Valid"
            return False, "Tampered Data"

        except Exception:
            return False, "Invalid Format"

# Example usage
if __name__ == "__main__":
    key = "APOLO_11_2026_SECRET"
    hb_manager = NetworkHeartbeat(key)

    # Simulate sending
    packet = hb_manager.generate_heartbeat()
    print(f"Generated Packet: {packet}")

    # Simulate receiving and verification
    is_valid, status = NetworkHeartbeat.verify_heartbeat(packet, key)
    print(f"Status: {status} | Valid: {is_valid}")
