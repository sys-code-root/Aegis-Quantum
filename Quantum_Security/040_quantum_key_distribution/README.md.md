# Quantum Key Distribution BB84 Simulator (Project 040)

A quantum cryptography simulator implementing the BB84 protocol via
IBM\'s Qiskit framework to safely exchange cryptographic key material
using qubit superposition mechanics.

## Technical Explanation

-   **Superposition Encoding:** Uses Hadamard gates (*H*) to shift
    qubits into diagonal bases, creating quantum states that cannot be
    copied or measured by an eavesdropper without destroying the data.
-   **Basis Sifting Operations:** Simulates public channel negotiation
    where matching measurement filters are compared, discarding
    uncorrelated execution states.
-   **Quantum State Observation:** Leverages the *qasm_simulator* kernel
    to evaluate quantum circuit results dynamically.

## Problems Solved

1.  **Symmetric Key Distribution Vulnerabilities:** Solves the core flaw
    of classical key distribution by linking security directly to the
    laws of quantum mechanics rather than mathematical complexity.
2.  **Eavesdropping Interference:** Any interception attempt (Eve)
    collapses the wave function, inducing a testable error rate that
    alerts both operators instantly.

## Usage

from 040_quantum_key_distribution import QuantumBB84\
\
\# Initialize a 32-qubit key exchange pipeline\
qkd = QuantumBB84(32)\
\
\# Generate the shared key\
secure_key = qkd.execute_exchange()
