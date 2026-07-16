# DNS Anomaly Detector

This script inspects domain names to flag suspicious patterns often associated with automated lookups or data exfiltration. It solves the need to quickly evaluate a list of domains by running checks on character length and digit distribution directly from the command line.

## What It Solves

* Evaluates domain text strings against a standard length threshold (defaults to 25 characters).
* Detects high ratios of numerical characters, flagging domains where more than 30% of the string consists of digits.
* Generates a shortened 16-character hexadecimal fingerprint for tracking scanned domains.

## Technical Choices

* Written in Python 3 using standard library modules, running without any external package installations.
* Uses the built-in re module to count digits inside domain strings using character matching.
* Uses the hashlib module to generate SHA-256 hashes, slicing the result to create a compact fingerprint.

## Prerequisites

You only need Python 3 installed on your system. No extra libraries are required.

## How to Run

Save the script as `dns_detector.py` and execute it from your terminal:

```bash
python dns_detector.py