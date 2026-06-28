# Integrated Quantum Attack & Defense Suite (Project 044)

A high-assurance, end-to-end security simulation platform engineered to model the complete lifecycle of quantum-secure communications. This suite bridges the architectural divide between mathematical state preparation, adversarial Grover-class cryptanalytic acceleration, and proactive Post-Quantum Cryptography (PQC) validation, providing a comprehensive sandbox for cryptographic risk assessment.

## Technical Explanation

* **State-Vector Superposition Engine:** Employs optimized linear algebra structures via NumPy to represent discrete quantum states. By computing the matrix Kronecker products and applying Hadamard ($H$) transformations, the engine simulates pure uniform superposition pipelines, mapping state-vector evolution without the dependency of external cloud hardware.
* **Grover Cryptanalytic Acceleration:** Models the probabilistic search space reduction matching Grover's optimization algorithm. The component simulates how non-linear amplitude amplification systematically bypasses classical brute-force checking, demonstrating the transition to an $\mathcal{O}(\sqrt{N})$ time-complexity bound in a controlled, multi-phase threat lifecycle.
* **Collision-Resistant Hardening:** Deploys an immutable, post-quantum verification layer leveraging forward cryptographic hash cascades (SHA-256). By anchoring the security boundary onto the preimage resistance of the compression algorithm, the defense layer immunizes transactional identity tokens against both Shor's factoring shortcut and Grover's search speedups.

## Problems Solved

* **Fragmented Threat Visibility:** Unifies distinct, isolated quantum concepts (QKD, cryptanalysis, and PQC) into a single sequential simulation framework, allowing operators to visualize exactly how a security boundary degrades and recovers under active attack.
* **Asymmetric Key Degradation:** Validates the cryptographic balance between symmetric entropy erosion and hash-based signature resilience, providing empirical evidence of why specific bit-lengths remain secure against next-generation adversaries.
* **Operational Boundary Verification:** Implements structural interface checks across all deployment phases, forcing input validation profiles to remain intact throughout the entire data-transport lifecycle.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **State Simulation** | NumPy Matrix Arrays | Provides highly performant, deterministic execution of low-qubit registers locally, avoiding network latency and overhead from full cloud provider libraries. |
| **Attack Scope** | Parametric Phase Tracking | Instead of a generic brute-force wrapper, the suite tracks execution across strict operational phases to pinpoint the precise moment a keyspace drops entropy. |
| **Defense Primitive** | SHA-256 Cascade | A zero-trapdoor cryptographic standard. It completely bypasses the mathematical vulnerabilities of integer factoring and discrete logarithms found in RSA/ECC. |
| **Architecture** | Monolithic Pipeline Design | Consolidating the phases ensures tight state binding, meaning the defense mechanisms react directly to the metrics exposed by the attack engine in real-time. |



## Usage

This integrated suite acts as the central orchestration plane for multi-vector quantum risk modeling within the lab. Ensure the file is saved as `quantum_suite.py`.

### Programmatic Simulation

```python
from quantum_suite import QuantumSuite

# 1. Initialize the comprehensive attack/defense simulation environment
suite = QuantumSuite()

# 2. Execute Phases 1-4: Quantum state preparation and secure key exchange simulation
suite.phase_1_4_secure_exchange()

# 3. Execute Phases 5-7: Inject an adversarial Grover cryptanalytic search vector
# Parameter determines the target qubit state matrix to isolate
suite.phase_5_7_grover_attack(1)

# 4. Deploy Phase 6 Hardening: Enforce the post-quantum hash-based shield
# Wraps and validates the execution token against transactional tampering
suite.phase_6_pqc_defense("Auth_Token_Payload")
