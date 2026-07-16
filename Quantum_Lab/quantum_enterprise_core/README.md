# Quantum Core Execution Script

This script combines quantum circuit execution routines with post-quantum key encapsulation mechanisms. It solves the need to simulate quantum validation models, run blind computing tests, analyze risk distributions, and compile circuit structures into hardware-specific target layouts.

## What It Solves

* Runs blind computing steps by applying explicit phase rotations to a qubit held in a uniform superposition state.
* Verifies the authenticity of simulated quantum token states by matching measurement outputs against expected binary values.
* Models asset risk distributions across 1024 execution shots using parameterized Y-axis rotations and qubit entanglement.
* Optimizes and compiles logical circuits into hardware-specific structures, exporting the result using OpenQASM 3.0 syntax.
* Secures tracking data payloads by running a post-quantum key encapsulation mechanism.

## Technical Choices

* Written in Python 3 to link classical data routines directly with quantum software components.
* Uses the Qiskit framework to build quantum circuits, assign logical gates, and run optimization layers.
* Uses the Qiskit Aer library (`AerSimulator`) to handle simulation processing locally on your machine.
* Uses the `qiskit.qasm3` module to export optimized circuit instructions into clean hardware assembly strings.
* Uses the Open Quantum Safe module (`oqs`) to deploy the Kyber768 algorithm for post-quantum key configuration.
* Uses the NumPy library to handle rotational math parameters like fractions of Pi.

## Prerequisites

You need Python 3 along with Qiskit, Qiskit Aer, and NumPy installed on your local environment.

Install the main packages using pip:

```bash
pip install qiskit qiskit-aer numpy