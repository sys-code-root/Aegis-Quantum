# Hash-Based Signature Simulator (Project 043)

A prototype demonstrating the mechanics of Post-Quantum Cryptography
(PQC) using hash-based signature primitives, designed to be resistant to
the Shor\'s algorithm threat model.

## Technical Explanation

-   **Collision Resistance:** Unlike RSA which is vulnerable to integer
    factorization on quantum processors, this scheme relies on the
    preimage resistance of SHA-256, which remains secure.
-   **Secret-Message Binding:** Combines entropy (secret key) and data
    payload (message) to create an immutable cryptographic signature.
-   **One-Time Signature (OTS) Logic:** Mimics the core principle of
    Lamport signatures, where the security is derived from the inability
    of an attacker to invert the hash function.

## Problems Solved

1.  **Quantum Threat Mitigation:** Effectively replaces vulnerable
    asymmetric primitives (RSA/ECC) with quantum-resilient hashing
    logic.
2.  **Signature Integrity:** Ensures that data has not been tampered
    with, providing a foundational block for secure post-quantum
    communication.

## Usage

from 043_hash_based_signature import HashSignature\
\
\# Initialize identity\
pqc = HashSignature()\
\
\# Sign a sensitive data packet\
sig = pqc.sign_message(\"Auth Data\")\
\
\# Verify identity signature\
valid = pqc.verify(\"Auth Data\", sig)
