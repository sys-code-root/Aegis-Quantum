# Basis Encoding Quantum Mapper (Project 045)

A high-assurance data preprocessing utility designed to transform classical bit-strings into quantum register states. This component serves as the foundational state-preparation layer for Quantum Machine Learning (QML) workflows, mapping discrete binary structures directly onto quantum computational baselines.

## Technical Explanation

* **Quantum Basis Encoding:** Implements a deterministic mapping technique where a classical bit-string $x = (x_1, x_2, \dots, x_n)$ with $x_i \in \{0, 1\}$ is translated directly into the corresponding quantum computational basis state $|x\rangle = |x_1 x_2 \dots x_n\rangle$. This links classical data parameters to specific state-vector coordinates.
* **Pauli-X State Excitation:** Programmatically applies Pauli-X ($X$) gates to transition selected qubits from the foundational $|0\rangle$ ground state to the $|1\rangle$ excited state. The engine evaluates the classical input character-by-character, injecting excitation operators only where active bit flags are present.
* **Hilbert Space State Mapping:** Maps classical discrete data sets into high-dimensional Hilbert spaces. By storing information directly within the state configurations of the qubit array, it prepares the system registers for non-linear operations executed by downstream variational quantum circuits (VQCs).

## Problems Solved

* **Classical-to-Quantum Data Ingestion:** Bridges the structural divide between legacy silicon-based binary structures and the quantum registers required for native quantum computing processing.
* **QML Input Standardization:** Provides a clean, highly predictable input preparation interface required by quantum classifiers, distance estimators, and variational optimization algorithms.
* **Qubit Register Alignment:** Prevents configuration failures and sizing mismatches by checking that the allocated qubit register length precisely scales to match the incoming data payload constraints.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Encoding Model** | Basis Encoding | Simple and highly reliable for binary features. Unlike Amplitude Encoding, it maps bits directly to state locations without needing complex multi-controlled rotation gate configurations for basic logic payloads. |
| **Simulation Backend** | `AerSimulator` | Delivers rapid, low-latency state-vector simulations locally, removing external API dependencies and network overhead during the data ingestion pipeline. |
| **Excitation Control** | Conditional Gate Injection | Evaluates bit values sequentially and applies $X$ gates only when a 1 is detected, keeping the circuit depth optimized and minimizing unnecessary execution instructions. |
| **Architecture** | Stateless Transformation | The encoder does not store historical state data; it transforms strings dynamically on-demand, ensuring the preprocessor remains lightweight and performant. |

## Usage

This utility serves as the primary data ingestion engine for your quantum simulation pipeline. Ensure the file is saved as `basis_encoding.py`.

### Programmatic Integration

```python
from basis_encoding import QuantumEncoder

# 1. Map a classical binary payload to a 3-qubit register space
# The utility automatically scales the circuit to match the payload length
encoder = QuantumEncoder("101")

# 2. Execute the state preparation and run the local simulation
# Returns the computed state counts reflecting the basis mapping
output_states = encoder.run_simulation()
