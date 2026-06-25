# Quantum Oracle API Gateway (Project 057)

An enterprise-ready, asynchronous FastAPI microservice engineered to bridge classical web architectures with post-quantum environments. This gateway implements dynamic cryptographic signature negotiation (ML-DSA/Falcon) alongside non-linear Quantum Machine Learning (QML) transaction classification pipelines.

## Technical Explanation

* **Asynchronous Service Layer (`FastAPI` & `Uvicorn`):** Transforms computation-heavy quantum execution circuits into highly concurrent, low-latency HTTP REST API endpoints. By utilizing Python's `asyncio` paradigm, the gateway handles network I/O bound requests efficiently without blocking the event loop during circuit evaluation.
* **Adaptive Post-Quantum Negotiation (`liboqs`):** Interrogates the underlying host environment compilation flags at instantiation to dynamically bind the highest-priority NIST-standardized quantum-safe signature mechanism (e.g., `ML-DSA-65`, `Falcon-512`). It includes a deterministic classical fallback layer utilizing `SHA-256` cascades to guarantee service availability across heterogeneous environments.
* **Quantum Space Feature Mapping ($ZZFeatureMap$):** Projects classical, low-dimensional transaction metrics (such as monetary amounts and calculated risk coefficients) into a high-dimensional quantum Hilbert space. By assigning these features directly to non-linear rotation parameters within the qubit registers, the framework leverages quantum state-vector probabilities for anomaly detection.

## Problems Solved

* **Monolithic Quantum Isolation:** Bridges the architectural divide between low-level quantum simulation runtimes and standard enterprise networks, enabling distributed systems to query quantum state evaluations securely via standard JSON payloads.
* **Cryptographic Agility & Compliance Migration:** Decouples the signature backend from the networking route handlers. This abstraction allows seamless, zero-downtime upgrades from early cryptographic drafts (e.g., Dilithium) to permanent standardized post-quantum algorithms (`ML-DSA`) without forcing database or API schema rewrites.
* **Payload Validation Hardening:** Replaces unstructured, untyped parameter parsing with strict Pydantic data schemas, preventing data-type coercion vulnerabilities and ensuring transaction parameters conform to exact validation criteria before entering the quantum pipeline.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Framework** | FastAPI + Pydantic | Provides native ASGI concurrency, automatic OpenAPI documentation, and strict input serialization via typed Data Models. |
| **QML Mapping** | `ZZFeatureMap` (reps=1) | Introduces non-linear data entanglement vectors, making it highly effective at separating complex, interleaved transaction data points. |
| **Crypto Agility** | Priority Array Compiling | Guarantees future-proofing. As newer NIST standards release, they can be appended to the priority array without altering endpoint code. |
| **State Processing** | `AerSimulator` (shots=1024) | Balances computational latency with statistical accuracy; 1024 shots provide a clean probability distribution curve for data evaluation. |

## Usage

This microservice functions as the primary ingestion gateway for post-quantum transaction telemetry. Ensure the file is saved as `quantum_oracle_api.py`.

### Service Initialization

Deploy the gateway container or local process using Uvicorn:

```bash
python oracle_api.py
