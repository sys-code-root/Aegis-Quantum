# Amplitude Encoding Quantum Compressor (Project 046)

A high-assurance quantum data-density optimization utility engineered to map classical information arrays into the continuous amplitudes of a quantum state vector. This module achieves exponential data compression relative to the physical qubit count, serving as a critical state-preparation gateway for advanced Quantum Machine Learning (QML) and high-density quantum storage architectures.

## Technical Explanation

* **Quantum Amplitude Mapping:** Exploits the massive state space of quantum registers. While classical systems require discrete physical bits for every data point, an $n$-qubit quantum system inherently spans a Hilbert space of dimension $M = 2^n$. This utility maps an entire classical vector directly onto the complex coefficients $\alpha_i$ of the normalized quantum state:

$$\n|\psi\rangle = \sum_{i=0}^{M-1} \alpha_i |i\rangle\n$$

* **Strict $L_2$-Norm Normalization:** Enforces rigorous mathematical validation boundaries by computing and applying an $L_2$-norm normalization constraint ($\|\psi\|_2 = 1$). This processes the raw incoming classical dataset into a valid, unit-length probability distribution curve, preventing runtime state execution errors during wave-function compilation.
* **Logarithmic Physical Scaling:** Demonstrates state-vector compaction by transforming linear data requirements into logarithmic physical constraints. A massive dataset containing $2^n$ distinct classical floating-point metrics can be completely encapsulated within the parallelized structure of a single $n$-qubit register.

## Problems Solved

* **Classical Memory Bottlenecks:** Resolves the memory allocation limits found when handling high-dimensional classical data arrays (such as financial time-series, biometric vectors, or pixel matrices) by offloading their representation to compact quantum configurations.
* **QML Input Barrier Optimization:** Drastically reduces the physical qubit count required to feed variational quantum algorithms, lowering the hardware resource ceiling needed to execute complex quantum classifiers and optimization models.
* **Algorithmic State Initialization:** Replaces manual state-building steps with an automated, direct vector initialization routine that computes the necessary quantum gate structures on-the-fly.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Encoding Method** | Amplitude Encoding | Achieves exponential space efficiency ($2^n$ values in $n$ qubits). Unlike Basis Encoding, which requires $1$ qubit per classical bit, Amplitude Encoding maximizes data density per register. |
| **Execution Kernel** | `AerSimulator` | Delivers precision verification of complex amplitude matrices locally, ensuring exact state-vector tracking without network overhead or API throttling. |
| **Data Sanitation** | Pre-computation $L_2$ Filter | Automatically handles zero-vectors and normalizes inputs *before* circuit assembly, preventing Qiskit initialization faults from malformed classical parameters. |
| **Architecture** | Functional Circuit Factory | Decouples vector processing from hardware instantiation; the compressor returns a clean `QuantumCircuit` object ready for transport, transpilation, or injection. |



## Usage

This utility functions as the primary data-compactor and ingestion component for high-density quntum pipelines. Ensure the file is saved as `amplitude_encoding.py`.

### Programmatic Integration

```python
from amplitude_encoding import QuantumCompressor

# 1. Instantiate the compressor with a high-dimensional classical array
# The array length must scale or be padded to a power of 2
raw_data = [1.0, 2.0, 3.0, 4.0]
compressor = QuantumCompressor(raw_data)

# 2. Automatically normalize the payload and construct the initialization circuit
# Maps 4 classical data coordinates onto a compact 2-qubit register
circuit = compressor.encode()
