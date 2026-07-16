# E91 Quantum Protocol Simulator

This script simulates the foundational steps of the E91 quantum key distribution protocol. It solves the need to model and test quantum entanglement generation and correlation measurements across shared communication channels using specified gate rotation angles.

## What It Solves

* Generates an entangled qubit pair (Bell state) using a combination of Hadamard and Controlled-NOT gates.
* Simulates independent measurement operations by applying parameterized Y-axis rotations for each communication side.
* Runs a multi-shot simulation to output a clear frequency count of resulting binary combinations.
* Verifies measurement distributions based on the chosen geometric angle alignment (0 and Pi/4).

## Technical Choices

* Written in Python 3 for direct compatibility with standard quantum scripting libraries.
* Uses the Qiskit framework to structure the qubit registers, map tracking gates, and compile circuit instructions.
* Uses Qiskit Aer (`AerSimulator`) to execute vector state processing locally without remote hardware requirements.
* Uses the NumPy library to handle rotational math parameters such as Pi fractions.
* Collects output statistics over a default baseline of 1024 simulator runs to track stability.

## Prerequisites

You need Python 3 along with the Qiskit, Qiskit Aer, and NumPy packages installed.

Install the required modules using pip:

```bash
pip install qiskit qiskit-aer numpy