# DNS Anomaly Detector (Project 004)

A forensic security utility designed to identify potentially malicious DNS queries and detect data exfiltration vectors, specifically targeting DNS Tunneling techniques.

## Technical Explanation

* **Heuristic Anomaly Analysis:** Utilizes optimized Regular Expressions to calculate the ratio of numeric digits to alphabetic characters within subdomains. This effectively flags "high-entropy" domains that resemble encoded binary payloads rather than human-readable URLs.
* **Deterministic Fingerprinting:** Implements `SHA-256` hashing to create unique, indexable identifiers for every domain encountered. This enables security teams to instantly correlate anomalous traffic patterns across distributed log files.
* **Rapid Triage Logic:** Operates on length-threshold and randomness-ratio heuristics. By filtering out standard traffic based on these parameters, the engine reduces noise for security analysts during the triage phase.

## Problems Solved

* **Data Exfiltration Detection:** Actively identifies attempts to smuggle data out via DNS subdomains, a common bypass for firewalls that do not inspect DNS traffic.
* **Automated Alerting:** Provides a programmatic gateway to flag suspicious traffic, transforming raw logs into actionable intelligence for manual security review.
* **Log Correlation:** Generates consistent, fixed-length IDs for domains, ensuring that evidence of suspicious behavior can be tracked and indexed across disparate network datasets.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Heuristic Logic** | `re` (Regex) Module | Provides low-overhead, high-speed filtering capabilities, enabling real-time analysis of thousands of queries per second. |
| **Fingerprinting** | `SHA-256` (Truncated) | Produces a collision-resistant unique ID. Truncating to 16 chars provides an optimal balance between uniqueness and database indexing performance. |
| **Detection Algorithm** | Length/Randomness Ratio | DNS Tunneling tools (e.g., *iodine*, *dnscat2*) create distinct, high-entropy patterns. These heuristics act as the first line of defense before full packet inspection. |
| **Performance** | Modular Methods | By keeping logic in static methods, the detector avoids object instantiation overhead, allowing for seamless integration into high-frequency packet sniffers. |

## Usage

This utility is designed to be imported into your existing network monitoring pipelines. Ensure the file is saved as `dns_detector.py`.

```python
from dns_detector import DNSAnomalyDetector

# Initialize the detection engine
detector = DNSAnomalyDetector(max_length=25)

# Validate a domain against security heuristics
domain = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.attacker.com"
is_suspicious, reason = detector.is_suspicious(domain)

if is_suspicious:
    print(f"ALERT: {reason}")
    print(f"Domain Fingerprint: {detector.get_domain_fingerprint(domain)}")
