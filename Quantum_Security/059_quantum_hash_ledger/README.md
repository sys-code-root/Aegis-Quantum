# Quantum-Resistant Hash Ledger (Project 059)

A secure cryptographic transactional ledger utilizing the Lamport
One-Time Signature (OTS) scheme backed by true bit-by-bit Quantum Random
Number Generation (QRNG).

## Technical Explanation

-   **Lamport Signatures:** A digital signature scheme where a message
    hash is signed by revealing selected parts of a private key matrix
    based on the binary representation of the hash bits.
-   **True Random Seeding:** Avoids software-calculated pseudo-random
    sequences by sampling individual wave function state collapses
    (\$\\alpha\|0\\rangle + \\beta\|1\\rangle\$) over a simulated
    quantum framework.
-   **Shor\'s Algorithm Immunity:** Since the security properties scale
    exclusively with preimage and collision properties of SHA-256, it
    bypasses the weaknesses of factoring or elliptic curve math.

## Problems Solved

1.  **Ledger Disruption Defenses:** Hardens transactional histories
    against future quantum computers capable of forging standard ECDSA
    consensus keys.
2.  **Deterministic Guessing vectors:** Mitigates vulnerabilities linked
    to predictable key gen patterns by feeding state configurations
    using randomized quantum entropy bytes.

## Usage

from 059_quantum_hash_ledger import QuantumHashLedger\
\
\# Instantiate the hash ledger\
ledger = QuantumHashLedger()\
\
\# Generate keys, append and sign a data block\
ledger.add_block(\"Transaction_Data_Payload\")
