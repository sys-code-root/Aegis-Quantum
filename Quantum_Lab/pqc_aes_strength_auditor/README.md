# Post-Quantum Resistance Analyzer

This script estimates the theoretical time required to brute-force symmetric encryption keys under classical and quantum computing conditions. It solves the need to verify why certain key sizes become vulnerable when subjected to quantum search acceleration, specifically using Grover's algorithm.

## What It Solves

* Calculates the total number of operations required to crack a key using classical brute force.
* Calculates the reduced operational complexity brought by quantum computing, applying a square root reduction factor based on Grover's algorithm.
* Converts raw operational steps into an estimated timeline in years using a fixed operations-per-second baseline.
* Evaluates key bit sizes (testing 128 and 256 bits) and flags them as vulnerable or safe using a 100-year resistance threshold.

## Technical Choices

* Written in Python 3 using standard execution paths with no external package requirements.
* Employs explicit mathematical calculations to compute bit depth exponents ($2^{bits}$ for classical and $2^{bits/2}$ for quantum).
* Uses a hardcoded performance baseline of $10^{18}$ operations per second to simulate a highly advanced computing cluster.
* Uses Python's standard string formatting to output large year metrics in clean scientific notation.

## Prerequisites

You only need Python 3 installed on your system. No external libraries are required.

## How to Run

Save the script as `pqc_analyzer.py` and run it from your terminal:

```bash
python pqc_analyzer.py