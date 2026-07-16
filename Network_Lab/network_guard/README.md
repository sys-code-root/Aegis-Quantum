# Network Guard Tools

This script provides functional tools for basic network connection checking, text obfuscation, and data integrity verification. It solves the need to grab service banners, obfuscate plain text strings, confirm data packages are not modified, and encode binary data for data transmission.

## What It Solves

* Captures response banners from remote network services over raw TCP connections and hashes them into unique SHA-1 fingerprints.
* Obfuscates and restores plain text strings using a symmetrical bitwise XOR operation.
* Validates data integrity by comparing data packets against a known hash using timing-attack resistant comparison functions.
* Encodes raw data bytes into standard Base64 text representations safe for transmission over network lines.

## Technical Choices

* Written in Python 3 using standard library modules, meaning it runs immediately without any pip installations.
* Uses the socket module to build explicit connections to a target host and port with a strict 3-second timeout rule.
* Uses the hashlib module to calculate SHA-1 and SHA-256 hex signatures.
* Uses the hmac module to leverage the compare_digest function, protecting the verification routine against side-channel timing attacks.
* Uses the base64 module to safely handle conversion of raw binary segments into printable ASCII characters.

## Prerequisites

You only need Python 3 installed on your system. No external libraries are required.

## How to Run

Save the script as `network_guard.py` and run it from your terminal:

```bash
python network_guard.py