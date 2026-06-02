# DNS Anomaly Detector (Project 4)

A security utility designed to identify potentially malicious DNS
queries, helping to detect data exfiltration attempts through DNS
tunneling.

## Purpose

DNS is the backbone of network resolution but is frequently abused for
\"DNS Tunneling\"---where sensitive data is encoded into subdomains.
This tool acts as a lightweight filter to audit DNS logs and flag
domains that exhibit \"high-entropy\" (random) patterns or abnormal
lengths.

## Technical Explanation

-   **Heuristic Analysis:** Uses regular expressions to calculate the
    ratio of numeric digits to alphabetic characters, identifying
    domains that look like encoded payloads rather than human-readable
    URLs.
-   **Fingerprinting:** Uses *SHA-256* to create a deterministic ID for
    every domain encountered, allowing security teams to correlate
    blocked domains across different log files.

## Problems Solved

1.  **Data Exfiltration Detection:** Identifies attempts to smuggle data
    out via DNS subdomains.
2.  **Alerting:** Provides a programmatic way to flag \"weird\" traffic
    for manual security review.
3.  **Log Correlation:** Creates consistent IDs for domains, helping
    build a history of suspicious behavior.

## Design Decisions

  --------------------- --------------------- -----------------------------------------------------------------------------------------------------------------
  **Heuristic Logic**   Regex (*re* module)   Offers a low-overhead, high-speed way to filter thousands of DNS queries in real-time.
  **Fingerprint**       *SHA-256*             Provides a fixed-length string (truncated to 16 chars) which is perfect for database indexing.
  **Algorithm**         Length/Randomness     DNS Tunneling tools (like *iodine*) create very distinct patterns; length checks are the first line of defense.
  --------------------- --------------------- -----------------------------------------------------------------------------------------------------------------

## Usage

from project_4_dns_anomaly_detector import DNSAnomalyDetector\
\
detector = DNSAnomalyDetector()\
status, reason = detector.is_suspicious(\"exemplo.com\")\
\
if status:\
print(f\"ALERT: {reason}\")
