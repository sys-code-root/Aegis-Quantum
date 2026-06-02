# Basis Encoding Quantum Mapper (Project 045)

A machine learning data-preprocessor that transforms classical
bit-strings into quantum register states, serving as the foundational
step for Quantum Machine Learning (QML) workflows.

## Technical Explanation

-   **Basis Encoding:** A direct mapping technique where a classical bit
    \$x_i \\in {0, 1}\$ is converted into a quantum state
    \$\|x_i\\rangle\$.
-   **Pauli-X Transformation:** Uses X-gate rotations to transition
    qubits from the \$\|0\\rangle\$ ground state to the \$\|1\\rangle\$
    excited state based on the input binary sequence.
-   **Hilbert Space Mapping:** Translates high-dimensional classical
    vectors into quantum amplitudes, allowing algorithms to manipulate
    data in complex vector spaces.

## Problems Solved

1.  **Classical-to-Quantum Interface:** Bridges the gap between
    traditional silicon-based data (0s and 1s) and quantum registers
    required for advanced computation.
2.  **Data Preparation for QML:** Provides the necessary input format
    for variational circuits and quantum-enhanced optimization tasks.

## Usage

from 045_quantum_basis_encoding import QuantumEncoder\
\
\# Map binary payload \'101\' to a 3-qubit quantum state\
encoder = QuantumEncoder(\"101\")\
output_states = encoder.run_simulation()
