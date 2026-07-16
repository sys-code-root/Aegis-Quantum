# Quantum Neural Network Setup

This script sets up a basic parameterized quantum neural network (QNN) layer. It solves the need to initialize quantum circuit architectures where data inputs and trainable weight parameters are handled separately, allowing the circuit to connect with classical machine learning optimization loops.

## What It Solves

* Initializes a 2-qubit quantum circuit layout with separate parameter groups for data features and models weights.
* Uses parameter vectors to map raw data inputs onto qubits using Y-axis rotations.
* Establishes training fields by applying X-axis gate rotations driven by weight parameters.
* Implements an entangling Controlled-NOT (CX) gate to combine qubit states.
* Wraps the circuit layers inside a functional estimator object prepared for machine learning updates.

## Technical Choices

* Written in Python 3 to leverage modern quantum data frameworks.
* Uses the Qiskit library to arrange the qubits, add functional parameters, and handle execution layout drawing.
* Uses the Qiskit Machine Learning library to define the structural EstimatorQNN layer object.
* Employs ParameterVector to manage multiple dynamic values at once without configuring individual variable names manually.

## Prerequisites

You need Python 3 along with the core Qiskit and Qiskit Machine Learning packages installed.

Install the required libraries using pip:

```bash
pip install qiskit qiskit-machine-learning