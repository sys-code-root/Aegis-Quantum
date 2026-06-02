# E91 Entanglement-Based QKD Protocol (Project 054)

A quantum cryptography simulator deploying Artur Ekert\'s E91 protocol
via maximally entangled EPR pairs to generate secure key material and
safeguard communication channels.

## Technical Explanation

-   **Bell Pair Generation:** Creates a state of maximum quantum
    correlation where individual qubits have no definite value until
    observed, but measurements remain perfectly linked.
-   **Basis Rotations:** Implements arbitrary \$R_y(\\theta)\$
    transformations to allow asymmetric basis tests, mimicking
    real-world tests for eavesdropping detection.
-   **Modern Compilation Pipeline:** Explicitly utilizes *transpile()*
    before code delivery, adhering to standard compilation optimization
    rules for modern quantum environments.

## Problems Solved

1.  **Source-Independent Security:** Because security is proven by
    testing correlation bounds, it does not matter if the hardware
    generating the qubits is untrusted or compromised.
2.  **Interception Containment:** Any external interaction collapses the
    state vectors instantly, ruining the correlation stats and raising
    an immediate defense alert.

## Usage

from 054_e91_entanglement_protocol import E91ProtocolSimulator\
\
\# Launch protocol simulation execution sequence\
e91_engine = E91ProtocolSimulator()\
counts = e91_engine.run_simulation(shots=2048)
