# Quantum Cryptography and Attack Simulator

This script simulates a multi-phase quantum security lifecycle. It solves the need to demonstrate basic quantum superposition state generation, simulate quantum-accelerated brute-force attacks, and apply post-quantum hashing to protect data bits.

## What It Solves

* Simulates initial key generation by creating a random bit and shifting its base state into a uniform quantum superposition vector.
* Simulates an attacker using Grover amplitude amplification to guess the hidden bit with a high probability model.
* Deploys a post-quantum cryptographic shield by hashing the target data with a classical, quantum-resistant hash algorithm.

## Technical Choices

* Written in Python 3 for straight terminal compatibility.
* Uses the NumPy library to handle linear algebra calculations, specifically defining a 2x2 Hadamard gate matrix and executing dot products for state transformations.
* Uses the standard random module to pick binary states and simulate the probability of attack success.
* Uses the hashlib module to generate standard SHA-256 hex signatures as a quantum-safe defensive measurement.

## Prerequisites

You need Python 3 and the NumPy library installed on your system.

Install the library using pip:

```bash
pip install numpy