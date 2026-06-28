# E91 Entanglement-Based QKD Protocol (Project 054)

A high-assurance quantum cryptography simulation platform implementing Artur Ekert's foundational E91 Quantum Key Distribution (QKD) protocol. Engineered using the modern Qiskit 1.x framework, this utility simulates the secure generation and exchange of cryptographic keys using maximally entangled Einstein-Podolsky-Rosen (EPR) pairs, linking transmission security directly to the statistical validation of quantum non-locality.

## Technical Explanation

* **Maximally Entangled EPR Pair Generation:** Populates a two-qubit register into a maximally entangled singlet state (Bell state $|\psi^-\rangle$). By applying a Hadamard ($H$) gate followed by a Controlled-NOT ($CX$) transformation and phase adjustments, the system creates an immutable non-local correlation where neither qubit holds a definite value until physical measurement occurs:

$$\n|\psi^-\rangle = \frac{|01\rangle - |10\rangle}{\sqrt{2}}\n$$

* **Asymmetric Basis Rotations ($R_y$):** Implements arbitrary Pauli-Y coordinate transformations ($R_y(\theta)$) to rotate measurement filters through specialized angles. This architecture enables Alice and Bob to select from three distinct, non-orthogonal bases, establishing the exact spatial configurations required to evaluate Clauser-Horne-Shimony-Holt (CHSH) inequality bounds.
* **Modern Qiskit 1.x Transpilation Pipeline:** Enforces modern quantum compilation constraints. The simulator explicitly routes the quantum execution graph through the native `transpile()` engine before submitting the payload to the local `AerSimulator`, optimizing gate depth and maintaining consistency with real physical hardware requirements.

## Problems Solved

* **Compromised Source Vulnerability (Untrusted Hardware):** Solves the single-point-of-failure flaw of standard QKD (like BB84) where the key emitter must be completely trusted. Because E91 verifies security through the non-local statistical correlation of the pairs, it detects compromises even if the particle generator was built or intercepted by a malicious adversary.
* **Passive Eavesdropping Vectors (Monogamy of Entanglement):** Instantly isolates interception attempts ($Eve$). Due to the Monogamy of Entanglement, any unauthorized third-party measurement breaks the pure entanglement between Alice and Bob, collapsing the wave function and preventing a statistical violation of Bell's inequality ($S \le 2$), which instantly triggers an infrastructure alert.
* **Legacy Provider Deprecation:** Replaces deprecated legacy simulation pipelines with the unified, thread-safe primitives of Qiskit 1.x, preventing execution failures across local high-performance nodes.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Protocol Foundation** | Entanglement-Based (E91) | Provides a superior security layer compared to prepare-and-measure variants by allowing absolute security validation over untrusted distribution hardware via Bell's Theorem. |
| **State Vector Model** | Singlet Anti-correlated State | Ensures that whenever Alice and Bob measure along matching bases, they achieve perfectly inverted results, maximizing downstream secret key generation entropy. |
| **Security Validation** | CHSH Inequality Auditing | Offers a mathematical proof of privacy. Computing the correlation coefficient establishes an empirical test for intercept detection. |
| **Compilation Scheme** | Pre-execution Transpilation | Manages physical gate mapping explicitly, isolating quantum logic anomalies before the instructions hit the simulation backend. |

## Usage

This utility serves as the primary entanglement-based distribution module for your quantum-hardened networking suites. Ensure the file is saved as `e91_protocol.py`.

### Programmatic Integration

```python
from e91_protocol import E91ProtocolSimulator

# 1. Initialize the E91 entanglement protocol simulation suite
# This provisions the internal registers and configures the asymmetric bases
e91_engine = E91ProtocolSimulator()

# 2. Execute the EPR generation, base selection, and sifting loops
# Returns the final measurement counts used for key material extraction and CHSH validation
counts = e91_engine.run_simulation(shots=2048)
