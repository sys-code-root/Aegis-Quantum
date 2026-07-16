# Quantum Data Compressor

This script converts classical data vectors into quantum state amplitudes. It solves the need to map digital arrays into an exponential quantum state space, optimizing how data is represented by using log2(N) qubits for a list of N numerical inputs.

## What It Solves

* Automatically computes the number of qubits required based on the size of the input list.
* Calculates the Euclidean norm of the data array to perform vector normalization.
* Encodes normalized numerical values directly into the amplitudes of a quantum circuit.
* Draws a text-based circuit layout directly to the terminal screen to show the initialization block.

## Technical Choices

* Written in Python 3 for direct compatibility with scientific computing modules.
* Uses the NumPy library to execute vector operations, compute structural norms, and calculate base-2 logarithms for circuit sizing.
* Uses the Qiskit framework to define the underlying quantum circuit components.
* Uses the native Qiskit initialization function to generate state preparation routines for the target inputs.

## Prerequisites

You need Python 3 along with the NumPy and Qiskit libraries installed.

Install the required packages using pip:

```bash
pip install numpy qiskit