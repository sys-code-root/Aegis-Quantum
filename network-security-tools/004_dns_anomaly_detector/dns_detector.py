import hashlib
import re

class DNSAnomalyDetector:

    def __init__(self, max_length=25):
        self.max_length = max_length

    def is_suspicious(self, domain):
        if len(domain) > self.max_length:
            return True, "Abnormal length"

        digit_count = len(re.findall(r'\d', domain))
        if digit_count / len(domain) > 0.3:
            return True, "High character randomness"

        return False, "Clean"

    @staticmethod
    def get_domain_fingerprint(domain):
        return hashlib.sha256(domain.encode()).hexdigest()[:16]

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
