# Quantum Neural Network (QNN) Setup (Project 052)

A high-assurance Quantum Machine Learning (QML) initialization framework engineered to construct variational Quantum Neural Networks (QNN). Built upon modern Qiskit Primitives, this utility leverages the `EstimatorQNN` abstraction to compute quantum expectation values, establishing a scalable, differentiable input layer optimized for hybrid classical-quantum optimization pipelines.

## Technical Explanation

* **Estimator Primitives Infrastructure:** Utilizes the unified Qiskit Primitives interface via `EstimatorQNN`. Instead of relying on raw stochastic shot counts to infer states, the engine calculates the analytical expectation values $\langle \hat{O} \rangle$ of target quantum observables, providing stable gradients required for backward-propagation loops.
* **Feature Map vs. Ansatz Separation:** Structural enforcement of the QML data pipeline. The framework clearly isolates the data-encoding layer (Feature Map), which translates classical inputs into specific Hilbert space coordinates, from the parameterized variational layer (Ansatz), containing the trainable weight matrices of the neural network.
* **Correlational Entanglement Fabrics:** Employs Controlled-NOT ($CX$) gates to inject non-local correlations across the qubit register. This multi-qubit entanglement allows the network to capture complex, non-linear feature interactions and high-dimensional cross-correlations that remain mathematically invisible to classical linear architectures.

## Problems Solved

* **Parameter Vector Scalability Bottlenecks:** Replaces single, manual variable declarations with Qiskit's `ParameterVector` architecture, enabling the programmatic construction of deep, multi-layered quantum neural layers with hundreds of input features and weights.
* **Hybrid Framework Interoperability:** Bridges the operational gap between quantum circuit graphs and classical deep learning ecosystems, formatting the quantum output tensor so it can be ingested natively by gradient-based optimization pipelines (such as PyTorch or TensorFlow workflows).
* **Gradient Phase Degradation:** Standardizes expectation-value tracking, minimizing the variance spikes typical of legacy sampling routines and stabilizing training convergence over non-convex cost surfaces.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **QNN Primitive** | `EstimatorQNN` | Computes exact continuous expectation values $\langle \hat{O} \rangle$, which are mathematically superior for regression and classification loss functions compared to discrete probability distributions from `SamplerQNN`. |
| **Variable Management** | `ParameterVector` | Allows dynamic layer scaling. Tracks features and weight indices programmatically within contiguous arrays, preventing namespace collisions during automated circuit transpilation. |
| **Entanglement Topology** | Linear CNOT Entangler | Keeps total circuit depth and gate counts low, matching the limitations of NISQ-era hardware while ensuring sufficient information flow across neighboring qubits. |
| **Execution Path** | Primitive-Driven Transpilation | Enforces modern Qiskit runtime structures, preparing the abstract network layer for instant deployment to physical quantum hardware providers or local high-performance simulators. |

## Usage

This utility serves as the primary initialization plane for constructing trainable quantum layers inside your hybrid analytical suites. Ensure the file is saved as `neural_setup.py`.

### Programmatic Integration

```python
from neural_setup import QuantumNeuralNetworkSetup

# 1. Initialize the network builder with target feature and weight dimensions
# This dynamically provisions the internal ParameterVectors and register blocks
builder = QuantumNeuralNetworkSetup(n_inputs=2, n_weights=2)

# 2. Extract the unified EstimatorQNN primitive instance
# Ready to be wrapped by classical deep learning connectors (e.g., TorchConnector)
qnn = builder.get_qnn()

print("[*] Quantum Neural Network layer successfully initialized.")
