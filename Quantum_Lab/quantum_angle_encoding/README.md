# Quantum Angle Encoder

This script converts classical numerical feature vectors into quantum states using angle encoding. It solves the need to map a set of continuous data points, such as sensor outputs, directly onto the rotation metrics of individual qubits for processing in quantum simulation environments.

## What It Solves

* Dynamically creates a quantum circuit allocation based on the total number of features in the input list.
* Maps continuous classical values directly to qubit states by applying parameterized Y-axis rotations.
* Measures all qubit values simultaneously to extract quantum state outcome distributions.
* Executes the configured quantum circuit on a local simulator backend to verify state preparation values.

## Technical Choices

* Written in Python 3 for seamless integration with scientific and data processing modules.
* Uses the Qiskit framework to structure the quantum circuit, handle qubit indexing, and compile the operational layers.
* Uses Qiskit Aer (`AerSimulator`) to emulate quantum execution states locally without relying on remote quantum hardware access.
* Employs RY rotation gates (`qc.ry`) to transition qubit states from the baseline state based on the provided numeric features.
* Uses the NumPy library to provide standard mathematical constants like Pi for input feature testing.

## Prerequisites

You need Python 3 along with the NumPy, Qiskit, and Qiskit Aer libraries installed.

Install the required packages using pip:

```bash
pip install numpy qiskit qiskit-aer