# Network Heartbeat Signer

This script creates and validates time-sensitive network heartbeat packets. It solves the need to ensure that dynamic status pings or messages passed between components are genuine, have not been modified in transit, and are not old messages being replayed.

## What It Solves

* Packet Signature: Combines a shared secret key with a current UNIX timestamp to generate a unique SHA-256 hash signature.
* Expiration Tracking: Checks the timestamp embedded inside incoming packets and rejects them if they fall outside a strict time window (default is 5 seconds).
* Alteration Detection: Re-calculates the expected hash signature on the receiving end to catch tampered payloads or modified timestamps.

## Technical Choices

* Written in Python 3 using only native modules, meaning it requires zero external library installations.
* Uses the hashlib module to generate secure SHA-256 hexadecimal string hashes.
* Uses the time module to grab and calculate absolute epoch differences for the validity window checks.
* Uses the secrets module to run the `compare_digest` string comparison method, which protects the verification checks from side-channel timing attacks.

## Prerequisites

You only need Python 3 installed on your system. No extra libraries are required.

## How to Run

Save the script as `network_heartbeat.py` and execute it from your terminal:

```bash
python network_heartbeat.py