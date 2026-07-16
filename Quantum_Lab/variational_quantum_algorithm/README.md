# Variational Quantum Optimizer

This script implements a basic variational quantum optimization loop. It solves the problem of tuning a parameterized quantum gate iteratively by linking a local quantum simulator to a classical optimization algorithm to minimize a specific measurement outcome probability.

## What It Solves

* Builds a single-qubit circuit utilizing a parameterized Y-axis rotation gate followed by a global measurement step.
* Defines an objective function that evaluates the circuit using a specific angle and calculates the target probability of measuring the 0 state.
* Feeds execution results into a classical optimization loop to find the specific rotation angle that minimizes the objective cost.
* Logs the final optimized rotation value in radians alongside the remaining error score.

## Technical Choices

* Written in Python 3 to bridge quantum operations with classical numerical analysis packages.
* Uses the Qiskit framework to model the parameter placeholder and assemble the underlying circuit layers.
* Uses the Qiskit Aer library to evaluate quantum state measurements locally using the AerSimulator module over 1024 execution shots.
* Uses the SciPy package to apply the COBYLA optimization method, which updates the angle values iteratively without requiring gradient calculations.
* Uses NumPy for internal numerical support during processing stages.

## Prerequisites

You need Python 3 installed along with Qiskit, Qiskit Aer, SciPy, and NumPy.

Install all required packages using pip:

```bash
pip install qiskit qiskit-aer scipy numpy