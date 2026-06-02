# Amplitude Encoding Quantum Compressor (Project 046)

A quantum data-density optimization utility that maps classical vectors
into quantum amplitudes, allowing for exponential storage compression
relative to qubit count.

## Technical Explanation

-   **Amplitude Mapping:** Unlike classical registers that hold one
    state, a quantum state \$\|\\psi\\rangle = \\sum\_{i=0}\^{N-1}
    \\alpha_i \|i\\rangle\$ stores \$N\$ amplitudes. This utility maps
    classical vector components directly to these \$\\alpha_i\$
    coefficients.
-   **Normalization Requirements:** Enforces L2-norm constraints
    (\$\|\|\\psi\|\| = 1\$), ensuring the quantum state vector remains a
    valid probabilistic distribution.
-   **Exponential Scaling:** Demonstrates the ability to store \$2\^n\$
    classical values within an \$n\$-qubit quantum register.

## Problems Solved

1.  **Memory Bottlenecks:** Enables the representation of large
    classical datasets (like images or financial vectors) in extremely
    compact quantum registers.
2.  **QML Input Efficiency:** Reduces the number of qubits required for
    quantum algorithms, effectively lowering the hardware barrier for
    executing quantum machine learning models.

## Usage

from 046_amplitude_encoding import QuantumCompressor\
\
\# Store 4 points in 2 qubits\
compressor = QuantumCompressor(\[1.0, 2.0, 3.0, 4.0\])\
circuit = compressor.encode()
