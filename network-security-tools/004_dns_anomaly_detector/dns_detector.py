import hashlib
import re

class DNSAnomalyDetector:
    """
    Analyzes domain names to detect potential DNS Tunneling or malicious exfiltration
    based on entropy and character length.
    """

    def __init__(self, max_length=25):
        self.max_length = max_length

    def is_suspicious(self, domain):
        """
        Determines if a domain is suspicious based on length and entropy.
        """
        # Rule 1: Abnormal length
        if len(domain) > self.max_length:
            return True, "Abnormal length"

        # Rule 2: High character randomness (simplified entropy check)
        # Malicious domains often use base64-like strings (e.g., a1b2c3d4.attacker.com)
        digit_count = len(re.findall(r'\d', domain))
        if digit_count / len(domain) > 0.3:
            return True, "High character randomness"

        return False, "Clean"

    @staticmethod
    def get_domain_fingerprint(domain):
        """Generates a SHA-256 hash of a domain for log correlation."""
        return hashlib.sha256(domain.encode()).hexdigest()[:16]

# Example usage
if __name__ == "__main__":
    detector = DNSAnomalyDetector()

    test_domains = [
        "google.com", 
        "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.attacker.com"
    ]

    for d in test_domains:
        suspicious, reason = detector.is_suspicious(d)
        print(f"Domain: {d} | Status: {reason if suspicious else 'Safe'}")
        print(f"Fingerprint: {detector.get_domain_fingerprint(d)}")
