# Quantum-Resistant Hash Ledger

This script implements a basic prototype of a quantum-resistant ledger that secures transactions using a hash-based one-time signature scheme. It solves the problem of protecting transaction data against quantum computing decryption threats by using the Lamport signature method driven by simulated quantum entropy.

## What It Solves

* Generates random data bytes by measuring a 1-qubit circuit placed in a uniform superposition via a Hadamard gate.
* Combines individual quantum bits using bit-shifting operations to assemble raw key blocks.
* Implements the Lamport signature scheme, creating public and secret key pairs out of 256-bit SHA-256 hash sets.
* Signs text transactions by matching the bits of the message hash with specific segments of the secret key array.
* Validates signature blocks against public keys to prevent identity spoofing or modification of the ledger data.

## Technical Choices

* Written in Python 3 for straight execution inside standard terminal environments.
* Uses the Qiskit library to define structural quantum circuits and track individual qubit measurement operations.
* Uses Qiskit Aer (`AerSimulator`) to execute local circuit simulation logic over single-shot runs.
* Uses the native hashlib library to compute standard SHA-256 digests for key generation and validation steps.
* Packages transaction information into local list arrays acting as a foundational blockchain model.

## Prerequisites

You need Python 3 along with the Qiskit and Qiskit Aer packages installed on your system.

Install the required modules using pip:

```bash
pip install qiskit qiskit-aer