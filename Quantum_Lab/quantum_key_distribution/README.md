# Quantum BB84 Key Distribution Simulator

This script simulates the BB84 Quantum Key Distribution protocol. It solves the need to demonstrate or test quantum cryptographic communication principles locally by mimicking how a shared secure key is generated and filtered across simulated quantum channels.

## What It Solves

* Automatically generates a random sequence of raw bits and polarization bases for the sender (Alice).
* Encodes bits into quantum states using single-qubit circuits with Pauli-X and Hadamard gates.
* Simulates random basis selections and single-shot measurements for the receiver (Bob).
* Filters out bits where the chosen bases do not match, leaving a final identical shared secret key string.

## Technical Choices

* Written in Python 3 for easy terminal testing.
* Uses the Qiskit framework to design individual quantum circuits representing transmitted qubits.
* Uses Qiskit Aer (`AerSimulator`) to handle local quantum circuit execution and extract measurement statistics.
* Uses the standard random module to handle classical bit generation and basis choices.
* Uses Qiskit's transpile function to optimize and prepare the circuits for the simulation backend.

## Prerequisites

You need Python 3 along with the Qiskit and Qiskit Aer libraries installed on your machine.

Install the required libraries using pip:

```bash
pip install qiskit qiskit-aer