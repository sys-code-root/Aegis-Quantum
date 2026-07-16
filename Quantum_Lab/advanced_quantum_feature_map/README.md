# Quantum Feature Map Encoder

This script converts classical numerical data vectors into quantum states using a non-linear data mapping layout. It solves the need to project standard feature lists into a quantum state space, creating data-dependent correlations across multiple qubits.

## What It Solves

* Instantiates a structured quantum circuit blueprint using the standard ZZFeatureMap model.
* Automatically handles feature dimensions and layer repetitions based on setup parameters.
* Configures a linear entanglement routine to link adjacent qubits together during the encoding stage.
* Binds floating-point raw numbers to symbolic gate parameters dynamically at runtime.
* Outputs a clear text-based ASCII diagram of the built circuit directly to the terminal.

## Technical Choices

* Written in Python 3 for straight terminal execution and compatibility with modern math packages.
* Uses the Qiskit library to leverage pre-built circuit library architectures like ZZFeatureMap.
* Employs the native assign_parameters method to map classical input vectors directly to structural gate angles.
* Uses the NumPy library to support internal array configurations.

## Prerequisites

You need Python 3 along with the Qiskit and NumPy libraries installed on your machine.

Install the required modules using pip:

```bash
pip install qiskit numpy