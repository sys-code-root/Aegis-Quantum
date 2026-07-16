# Quantum Binary Encoder

This script converts classical binary strings into quantum states using basis encoding. It solves the need to map standard digital input data into a quantum circuit representation so it can be processed by quantum simulator backends.

## What It Solves

* Dynamically scales a quantum circuit based on the length of the input binary string.
* Reads each bit of the classical string and applies a state flip to the corresponding qubit if the value is 1.
* Measures the entire quantum register to verify that the states match the original input.
* Runs the setup on a local simulator to output the resulting configuration counts.

## Technical Choices

* Written in Python 3 for quick integration with modern quantum development packages.
* Uses the Qiskit framework to build, track, and scale the structural quantum circuits.
* Uses Qiskit Aer (`AerSimulator`) to run local state measurements without needing connection to physical quantum hardware.
* Employs Pauli-X gates (`qc.x`) to handle basis state initialization by shifting qubits from the ground state 0 to 1.
* Executes the simulation using 1024 distinct shots to confirm stability and accuracy.

## Prerequisites

You need Python 3 along with the Qiskit and Qiskit Aer libraries installed.

Install the required packages using pip:

```bash
pip install qiskit qiskit-aer