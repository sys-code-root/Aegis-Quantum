# Quantum Hash Ledger Simulator

This script provides a basic implementation of a ledger that signs transactions using a hash-based one-time signature scheme. It solves the need to protect data entries against quantum computing threats by employing the Lamport signature method driven by simulated quantum randomness.

## What It Solves

* Simulates a quantum random number generator by setting a single qubit into a uniform superposition state using a Hadamard gate.
* Assembles random bytes using bitwise shift operations on individual quantum measurement outputs.
* Implements a Lamport signature model, generating secret and public key sets out of standard SHA-256 arrays.
* Signs text payloads by matching the bit values of a hashed message directly with corresponding secret key segments.
* Validates signature structures against public identifiers to ensure transaction records are authentic and have not been modified.

## Technical Choices

* Written in Python 3 for immediate deployment across standard command-line environments.
* Uses the Qiskit framework to design single-qubit quantum circuit components and track measurements.
* Uses Qiskit Aer (`AerSimulator`) to transpile and execute the simulation code locally using single-shot runs.
* Uses the native `hashlib` library to handle all SHA-256 cryptographic generation and validation steps.
* Uses bitwise operations (`<<`, `>>`) to convert raw data streams between individual bits and complete byte blocks.

## Prerequisites

You need Python 3 along with the Qiskit and Qiskit Aer packages installed.

Install the required modules using pip:

```bash
pip install qiskit qiskit-aer