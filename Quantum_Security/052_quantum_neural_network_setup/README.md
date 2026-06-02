# Quantum Neural Network (QNN) Setup (Project 052)

Initializes a variational QNN architecture using Qiskit Machine
Learning\'s *EstimatorQNN* primitive, designed for hybrid
quantum-classical integration.

## Technical Explanation

-   **Estimator Primitive:** Utilizes the Estimator interface, which is
    the Qiskit standard for calculating expectation values of quantum
    observables.
-   **Feature Map vs. Ansatz:** Clearly delineates between the
    data-encoding layer (Feature Map) and the learnable-weight layer
    (Ansatz), a core requirement for QML.
-   **Correlational Entanglement:** Employs the *CX* (CNOT) gate to
    establish entanglement between qubits, allowing the network to
    process data dependencies that are invisible to classical linear
    models.

## Problems Solved

1.  **Model Scalability:** Moving from single-parameter circuits to
    *ParameterVector* enables the creation of deep, multi-input neural
    networks.
2.  **Framework Compatibility:** Establishing the QNN primitive allows
    for gradient-based training using classical optimizers (like Adam or
    COBYLA) via standard ML libraries.

## Usage

from 052_quantum_neural_network_setup import QuantumNeuralNetworkSetup\
\
\# Initialize network\
builder = QuantumNeuralNetworkSetup(n_inputs=2, n_weights=2)\
qnn = builder.get_qnn()\
\
\# qnn object is now ready for training within a PyTorch or TensorFlow
workflow
