# Quantum Key Distribution BB84 Simulator (Project 040)

A high-assurance quantum cryptography simulation platform implementing the foundational BB84 Quantum Key Distribution (QKD) protocol. Engineered using the modern Qiskit 1.x framework, this utility simulates the secure exchange of cryptographic key material over a combination of quantum channels (using qubit state polarization) and classical channels, linking transport security directly to the laws of quantum mechanics.

## Technical Explanation

* **Dual-Basis Superposition Encoding:** Generates raw binary sequences mapped across two non-orthogonal quantum bases: rectilinear ($Z$) and diagonal ($X$). By programmatically applying Pauli-X ($X$) and Hadamard ($H$) gates, bits are encoded into quantum states that cannot be duplicated or eavesdropped upon without disrupting their mathematical state.
* **Classical Basis Sifting Operations:** Simulates the post-quantum public negotiation phase. After Bob performs measurements using randomized bases, Alice and Bob exchange their basis choices over an unsecure classical channel, filtering and discarding uncorrelated execution states to extract a pure, identical secret key.
* **Qiskit 1.x Native Compilation:** Utilizes the high-performance `AerSimulator` backend. The protocol logic enforces modern quantum software engineering compilation steps by transpiling each execution topology dynamically before runtime execution, guaranteeing precise state-vector results.

## Problems Solved

* **Mathematical Vulnerability in Key Exchange:** Eliminates the core risk of classical asymmetric key exchanges (like Diffie-Hellman or RSA), which rely on unproven computational hardness assumptions that will collapse under Shor's algorithm. QKD links security to the No-Cloning Theorem.
* **Passive Eavesdropping (Man-in-the-Middle):** Discovers interception attempts ($Eve$) automatically. Any unauthorized measurement collapses the superposition wave function, introducing a deterministic $25\%$ error rate per intercepted bit, instantly alerting both operators before key deployment.
* **Legacy Code Deprecation:** Solves the stability issues found in older QKD scripts by replacing the deprecated `Aer.get_backend('qasm_simulator')` with the unified, thread-safe execution environment of Qiskit 1.x.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Simulation Kernel** | `AerSimulator()` | Universal standard for Qiskit 1.x. Bypasses deprecated provider paths and executes rapid state calculation profiles with low memory footprints. |
| **State Mapping** | Dual-Basis System ($Z$ / $X$) | Adheres strictly to the physical BB84 specification, leveraging the Heisenberg Uncertainty Principle to make simultaneous measurement of conjugate properties impossible. |
| **Sifting Logic** | Classical Array Intersect | Maximizes entropy preservation. Public comparison of bases safely filters out noise, leaving a statistically sound, correlated secret key string. |
| **Architecture** | Independent Iteration Loops | Simulates sequential physical states. Each bit runs as a standalone quantum instance, mirroring real-world single-photon fiber execution networks. |



## Usage

This utility serves as the decentralized key exchange module for your secure communication pipelines. Ensure the file is saved as `quantum_bb84.py`.

### Programmatic Execution

```python
from quantum_bb84 import QuantumBB84

# 1. Initialize a 32-qubit key exchange pipeline
# This provisions the Qiskit execution backend
qkd = QuantumBB84(num_bits=32)

# 2. Execute state preparation, measurement, and sifting
# Returns the final synchronized post-quantum shared secret key
secure_key = qkd.execute_exchange()
