# Angle Encoding for Quantum Neural Networks (Project 047)

A high-assurance data-mapping utility engineered to translate continuous classical features into quantum register rotations. This module functions as the foundational, non-linear input layer for Variational Quantum Circuits (VQC) and Hybrid Quantum-Classical Neural Networks (QNN), enabling direct ingestion of real-valued floating-point metrics into state amplitudes.

## Technical Explanation

* **Parameterized Rotation Encoding:** Utilizes single-qubit rotation gates—specifically Pauli-Y rotations ($R_y(\theta)$)—to map continuous classical values directly into the probability amplitudes of the register. Each feature coordinate $\theta$ controls the exact probability distribution of the target qubit, transforming the ground state into a parameterized superposition:

$$\n|\psi\rangle = \cos\left(\frac{\theta}{2}\right)|0\rangle + \sin\left(\frac{\theta}{2}\right)|1\rangle\n$$

* **Linear Feature-to-Qubit Mapping:** Establishes a structured $1:1$ configuration map where each independent feature within a classical vector maps directly to an isolated physical qubit. This allows high-dimensional feature vectors to be represented in parallel across the register, optimizing execution speed during forward-propagation passes.
* **QNN Input Layer Abstraction:** Synthesizes the core interface boundary for hybrid classical-quantum machine learning models. By representing classical input vectors as structural rotation angles, it allows classical backpropagation optimization loops to compute gradients relative to down-stream variational parameters.

## Problems Solved

* **Continuous Feature Ingestion Gaps:** Resolves the limitation found in Basis Encoding (which requires discrete binary bitstrings) by allowing the network to natively ingest continuous, real-valued data fields without losing resolution through decimal-to-binary coercion.
* **Circuit Depth Inflation:** Minimizes total gate count during state preparation. Unlike Amplitude Encoding, which requires heavy multi-controlled rotation sequences, Angle Encoding completes initialization in a single parallel step, keeping circuit execution well within NISQ-era coherence limits.
* **Variational Optimization Instabilities:** Standardizes classical feature inputs into bounded rotational intervals, ensuring smooth probability distributions across the Hilbert space and preventing gradient scaling anomalies.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Encoding Method** | Angle Encoding via $R_y(\theta)$ | Eliminates complex phase variables by keeping state vector amplitudes strictly real-valued, making state verification and measurement tracking computationally efficient. |
| **Mapping Scaling** | Linear Allocation (1 feature : 1 qubit) | Maximizes parallel gate execution. It prioritizes low circuit depth over qubit conservation, preventing rapid phase degradation. |
| **Simulation Backend** | `AerSimulator` Core | Delivers rapid tracking of state-vector measurement probabilities locally, removing cloud-provider queuing times during multi-iteration neural network training. |
| **Data Normalization** | Radians Boundary Filter | Enforces pre-execution checking to ensure all incoming metrics are scaled properly, preventing aliasing issues caused by periodic rotation resets. |



## Usage

This utility serves as the primary feature-ingestion layer for your quantum neural network models. Ensure the file is saved as `angle_encoding.py`.

### Programmatic Integration

```python
import numpy as np
from angle_encoding import AngleEncoder

# 1. Prepare a continuous classical feature vector scaled to radians
normalized_features = [np.pi/4, np.pi/2, np.pi]

# 2. Instantiate the encoder to automatically allocate a 3-qubit register space
encoder = AngleEncoder(normalized_features)

# 3. Execute the state preparation and retrieve the measurement probabilities
probabilities = encoder.run_simulation()
