# Hash Signature Generator

This script provides a basic implementation of a hash-based message signing routine using symmetric functions. It solves the need to sign text payloads and verify data authenticity by binding a message to a securely generated secret key without relying on traditional asymmetric mathematical algorithms.

## What It Solves

* Generates a unique 32-byte secret key dynamically on initialization.
* Creates a corresponding public identifier by hashing the generated secret key.
* Signs text messages by combining the secret key data with the SHA-256 hash of the target message payload.
* Verifies signature integrity by recomputing the hash sequence on the receiving end to ensure the payload was not modified.

## Technical Choices

* Written in Python 3 using standard library modules, running without any external package dependencies.
* Uses the os module (`os.urandom`) to fetch 32 random bytes from the operating system's cryptographic entropy source.
* Uses the hashlib module to handle all underlying SHA-256 string and byte hashing operations.
* Encodes string inputs into raw bytes inside a dedicated internal helper function before running the hashing sequence.

## Prerequisites

You only need Python 3 installed on your system. No extra libraries are required.

## How to Run

Save the script as `hash_signature.py` and run it from your terminal:

```bash
python hash_signature.py