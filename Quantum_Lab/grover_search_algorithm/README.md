# Grover Search Simulator

This script simulates Grover's search algorithm on a 2-qubit quantum circuit. It solves the problem of searching an unstructured database of four items to find a specific marked item in a single operational step instead of checking items one by one classically.

## What It Solves

* Initializes a 2-qubit system to represent a search space of four possible states (00, 01, 10, and 11).
* Generates a uniform superposition so all states have an equal starting probability.
* Implements a quantum oracle that targets and flips the phase of the specific target state 11.
* Applies an amplitude amplification step to suppress the unwanted states and maximize the measurement probability of the marked target.

## Technical Choices

* Written in Python 3 for straight execution inside standard terminal environments.
* Uses the Qiskit framework to map out quantum circuit phases, gates, and measurement barriers.
* Uses the Qiskit Aer library to handle simulation routines locally through the AerSimulator backend.
* Runs the final compiled circuit with a configuration of 1024 execution shots to gather statistical measurement counts.

## Prerequisites

You need Python 3 along with the Qiskit and Qiskit Aer libraries installed.

Install the required packages using pip:

```bash
pip install qiskit qiskit-aer