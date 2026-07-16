# Quantum Oracle API Gateway

This project is a web API that runs a simulated quantum fraud analysis check on transactions and signs the results using quantum-safe signature algorithms. It solves the problem of integrating quantum-based data processing and post-quantum cryptography (PQC) validation into a standard HTTP web service.

## What It Solves

* Exposes a fast web endpoint to receive automated transaction entries containing financial and risk parameters.
* Feeds continuous values into a 2-qubit quantum feature map to check for anomalies based on state distribution probabilities.
* Identifies and selects the best available post-quantum signature algorithm installed on the host system to secure data outputs.
* Automatically falls back to standard classical SHA-256 hashing if post-quantum signature engines are missing or fail to load.

## Technical Choices

* Uses FastAPI to set up a minimal, asynchronous API server with low overhead.
* Uses Pydantic data models to enforce and validate structure on input JSON objects.
* Uses the Qiskit library along with `qiskit-aer` (`AerSimulator`) to configure and run feature data evaluations across 1024 simulation shots.
* Uses the Open Quantum Safe module (`oqs`) to dynamically search for and execute modern security signature schemes like ML-DSA or Dilithium.
* Uses Uvicorn as the native ASGI runner to power the service on a local network interface.

## Prerequisites

You need Python 3 along with the web framework, validation, and quantum computing modules installed.

Install the main packages using pip:

```bash
pip install fastapi pydantic uvicorn qiskit qiskit-aer