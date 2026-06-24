# Advanced Quantum Feature Maps (Project 053)

A high-assurance data-transformation framework engineered to implement multi-layered `ZZFeatureMap` architectures using Qiskit 1.x. This module projects continuous, real-valued classical feature vectors into deeply entangled quantum state vectors, laying the mathematical foundation for Quantum Support Vector Machines (QSVM) and advanced quantum kernel classification models.

## Technical Explanation

* **Quantum Kernel Trick Strategy:** Projects classical input metrics $x \in \mathbb{R}^d$ into a high-dimensional quantum Hilbert space, generating the state density matrix $|\Phi(x)\rangle\langle\Phi(x)|$. This non-linear mapping allows quantum classifiers to evaluate complex decision boundaries and hyperplanes that are computationally intractable to separate within classical data spaces.
* **Non-Linear Phase Rotaion Operators:** Employs single-qubit Pauli-Z rotations ($R_z$) and multi-qubit cross-correlation rotations ($R_{zz}$). The transformation maps individual features to independent qubit phases, while simultaneously computing high-order data interactions using the standard non-linear coupling function:

$$\phi(x_i, x_j) = (\pi - x_i)(\pi - x_j)$$

* **Entanglement Cascade Topologies:** Enforces data synchronization across the register utilizing a linear entanglement strategy. Interweaving Controlled-NOT ($CX$) gates between phase operations links adjacent feature variables, creating a highly complex, non-linear data signature that blocks reverse-engineering attempts by passive adversaries.

## Problems Solved

* **Classical Linear Separability Overheads:** Resolves classification failures found when analyzing overlapping or non-linearly separable classical datasets (such as concentric clusters or high-frequency market matrices) by scattering them into multi-dimensional orthogonal state combinations.
* **High-Order Correlation Dropping:** Captures subtle, high-degree relationships between data features ($x_i$ and $x_j$) that standard single-qubit encoding setups (like basic $Z$-axis maps) discard, maximizing the structural expressibility of the feature space.
* **Circuit Topology Drift:** Replaces brittle, manual loop-built gate constructions with the optimized, certified Qiskit `ZZFeatureMap` blueprint, ensuring native compliance with physical hardware transpilers.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Feature Map Type** | `ZZFeatureMap` | Selected over `ZFeatureMap` because it captures cross-feature correlations ($R_{zz}$ interaction layers), which is essential for capturing non-linear patterns in complex datasets. |
| **Entanglement Strategy** | Linear Cascade | Optimizes the balance between circuit depth and correlation tracking, preventing rapid phase noise accumulation on near-term hardware. |
| **Layer Repetitions** | Parameterized Execution (`reps=2`) | Doubles the encoding depth to maximize the expressibility and structural complexity of the quantum state without exceeding NISQ coherence limits. |
| **Data Scaling Gate** | Native $R_y$ Pre-activation | Prepares the register state prior to phase injection, ensuring features are mapped uniformly across the Bloch sphere's surface geometry. |



## Usage

This framework acts as the primary data-transformation and state-generation layer for your quantum-enhanced machine learning tasks. Ensure the file is saved as `quantum_feature_map.py`.

### Programmatic Integration

```python
from quantum_feature_map import QuantumFeatureMap

# 1. Initialize a 2-dimensional advanced quantum feature map
# Sets the structural layers to repeat the non-linear mapping twice
mapper = QuantumFeatureMap(feature_dimension=2, reps=2)

# 2. Encode a continuous classical data payload into the circuit graph
# Returns an optimized QuantumCircuit object ready for kernel estimation
quantum_data_circuit = mapper.encode_data([0.5, 1.2])
