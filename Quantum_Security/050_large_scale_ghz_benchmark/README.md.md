# Large Scale GHZ Benchmarking (Project 050)

A high-memory stress test simulation designed to evaluate classical
hardware limits by generating an entangled 30-qubit
Greenberger-Horne-Zeilinger (GHZ) state.

## Technical Explanation

-   **GHZ State:** A maximally entangled state that requires deep
    circuit depth and massive state-vector tracking.
-   **Exponential Scaling:** Because the state space of \$n\$ qubits is
    \$2\^n\$, a 30-qubit simulation requires tracking over \$10\^9\$
    complex amplitudes, pushing the limits of standard local memory.
-   **Simulator Efficiency:** Utilizes *qasm_simulator* over
    *statevector_simulator* to reduce total memory footprint during the
    measurement sampling phase.

## Problems Solved

1.  **Hardware Limit Assessment:** Establishes the \'ceiling\' of your
    current local development environment for quantum research.
2.  **Computational Bottleneck Identification:** Provides a baseline to
    compare performance between different simulator backends or hardware
    acceleration options.

## Usage

from 050_large_scale_ghz_benchmark import QuantumBenchmark\
\
\# Execute 30-qubit entanglement benchmark\
benchmark = QuantumBenchmark(30)\
benchmark.run_benchmark()
