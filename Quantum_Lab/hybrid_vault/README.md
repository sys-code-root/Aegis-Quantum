# Hybrid Cryptographic Vault Simulator

This script combines post-quantum key encapsulation with standard symmetric encryption to protect text data. It solves the need to secure data payloads using modern quantum-safe keys while leveraging a simulated quantum circuit to generate random entropy bytes for encryption initialization vectors.

## What It Solves

* Implements a hybrid data protection flow by using a quantum-resistant key setup alongside traditional block ciphers.
* Simulates a quantum random number generator (QRNG) to create unpredictable initialization vectors by measuring qubits placed in a superposition state.
* Secures a target message payload by running key encapsulation routines and symmetric encryption blocks sequentially.
* Processes string payloads into raw data bytes, handles required block padding, and outputs the resulting encrypted hex values to the command line.

## Technical Choices

* Written in Python 3 to merge quantum simulation toolkits with classical cryptographic libraries.
* Uses the Open Quantum Safe wrapper wrapper module (`oqs`) to run the Kyber768 key encapsulation mechanism.
* Uses the PyCryptodome library (`Crypto`) to handle standard AES encryption routines inside Cipher Block Chaining (CBC) mode.
* Uses the Qiskit framework and `qiskit-aer` (`AerSimulator`) to construct and run single-shot quantum registers utilizing Hadamard gates.

## Prerequisites

You need Python 3 along with the Qiskit, Qiskit Aer, PyCryptodome, and Open Quantum Safe core modules installed on your local machine.

Install the primary Python dependencies using pip:

```bash
pip install qiskit qiskit-aer pycryptodome