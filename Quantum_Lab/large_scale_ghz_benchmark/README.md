# Quantum Simulation Benchmark

This script benchmarks local hardware performance and system memory limits by running a 30-qubit quantum entanglement simulation. It resolves the need to stress-test computer processing speeds and verify if your machine can handle large state allocations before running heavy quantum algorithms locally.

## What It Solves

* Builds a 30-qubit quantum circuit to test hardware capabilities under intense computation requirements.
* Creates a multi-qubit entanglement chain using a single Hadamard gate followed by sequential Controlled-NOT (CX) gates.
* Tracks exact execution time during circuit compilation and processing using a 100-shot setup.
* Includes specialized memory error checks to safely alert the user if the system runs out of RAM instead of crashing the process.

## Technical Choices

* Written in Python 3 for direct compatibility with modern quantum development tools.
* Uses the Qiskit framework to organize qubit arrays, place logic gates, and handle compilation steps.
* Uses the Qiskit Aer library to execute the simulation locally using the native AerSimulator backend.
* Uses the standard time module to log the initial and final execution timestamps for benchmarking.

## Prerequisites

You need Python 3 along with the Qiskit and Qiskit Aer packages installed. Running a 30-qubit simulation requires approximately 16GB of free system RAM.

Install the required modules via pip:

```bash
pip install qiskit qiskit-aer