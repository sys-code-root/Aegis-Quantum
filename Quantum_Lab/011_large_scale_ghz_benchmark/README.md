# Large Scale GHZ Benchmarking (Project 050)

A high-assurance hardware stress-testing and benchmarking framework engineered to evaluate classical compute boundaries through large-scale quantum state simulation. This utility constructs a 30-qubit Greenberger-Horne-Zeilinger (GHZ) maximally entangled state, forcing the host execution platform to track dense multi-particle correlation matrices and mapping the literal limits of classical silicon under exponential quntum scaling.

## Technical Explanation

* **Maximally Entangled GHZ States:** Constructs the multi-particle entangled state topology across a 30-qubit register. By executing an initial initialization Hadamard ($H$) gate followed by a linear cascaded chain of Controlled-NOT (CNOT) operations, the circuit establishes a macroscopic superposition where all registers are perfectly correlated:

$$\n|\text{GHZ}\rangle = \frac{|0\rangle^{\otimes n} + |1\rangle^{\otimes n}}{\sqrt{2}}\n$$

* **Exponential Memory Space Complexity:** Drastically exposes the classical computational bottleneck. Because the dimensions of an $n$-qubit state vector scale at $M = 2^n$, executing a 30-qubit simulation demands that the classical system allocates, tracks, and processes $2^{30}$ complex floating-point amplitudes (exceeding $10^9$ coordinates), creating an aggressive benchmark for local RAM configurations.
* **AerSimulator Optimization:** Utilizes the high-performance native `AerSimulator` architecture over standard uncompressed state-vector engines. By injecting explicit measurement operators across the entire register array, the execution loop shifts from full matrix state dumps to optimized stochastic shot sampling, minimizing memory degradation and preventing immediate kernel panic events.

## Problems Solved

* **Classical Hardware Boundary Profiling:** Establishes a definitive, empirical performance ceiling for local development environments, showing exactly when a machine will exhaust its memory buffers during advanced quantum research.
* **Simulator Backend Bottleneck Isolation:** Provides a standardized baseline to benchmark execution latencies, cache performance, and multi-threading capabilities across varying compiler configurations or hardware acceleration layers (e.g., CPU vs GPU acceleration).
* **RAM Exhaustion Thrashing Preemption:** Protects production pipelines by validating execution resource requirements pre-flight, demonstrating how algorithmic structures behave before they are sent to physical quantum processing units (QPUs).

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **State Target** | 30-Qubit GHZ | The optimal structure for non-local stress testing. Unlike independent states, a GHZ state forces total global register entanglement, preventing the compiler from applying tensor-network truncation optimizations. |
| **Backend Target** | `AerSimulator()` | Selected for Qiskit 1.x compatibility. It handles parallel multi-threaded shot evaluation natively and scales robustly across local core layouts. |
| **Circuit Topology** | Linear CNOT Cascade | Maintains clear, traceable execution depth. The sequential step-by-step entanglement propagation makes it easy to monitor thread scaling during hardware audits. |
| **Data Evaluation** | Shot Sampling Mapping | Prevents out-of-memory crashes. Sampling bitstrings via shots avoids the necessity of storing the entire raw $2^{30}$ complex array in active memory. |



## Usage

This framework serves as the primary system stress-test utility for auditing local hardware nodes before dispatching dense quantum workloads. Ensure the file is saved as `ghz_benchmark.py`.

### Programmatic Benchmarking

```python
from ghz_benchmark import QuantumBenchmark

# 1. Initialize the 30-qubit GHZ entanglement stress test environment
# Automatically calculates the theoretical keyspace constraints
benchmark = QuantumBenchmark(num_bits=30)

# 2. Transpile the circuit graph and trigger the hardware stress loop
# Measures execution latency and reports system stability metrics
benchmark.run_benchmark()
